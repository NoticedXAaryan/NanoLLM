# train.py
# Main training loop for NanoLLM.
#
# Run with:  python train.py
#
# Training details:
#   - Mixed precision: bf16 (stable on Ampere GPUs)
#   - Gradient accumulation: simulates larger effective batch size
#   - LR schedule: linear warmup + cosine decay
#   - Gradient clipping: prevents exploding gradients
#   - Evaluation: val loss + sample generation every eval_interval steps

import os
import re
import json
import time
import torch
from config import model_config as mcfg, train_config as tcfg
from model import NanoLLM
from data import get_dataloaders
from tokenizer import get_tokenizer, encode, decode
from utils import cosine_lr_with_warmup, save_checkpoint, plot_loss_curve, log_to_jsonl


def format_time(seconds: float) -> str:
    """Format seconds into a human-readable string."""
    if seconds < 60:
        return f"{seconds:.0f}s"
    elif seconds < 3600:
        m, s = divmod(int(seconds), 60)
        return f"{m}m {s}s"
    else:
        h, remainder = divmod(int(seconds), 3600)
        m, s = divmod(remainder, 60)
        return f"{h}h {m}m {s}s"


def get_gpu_mem_mb() -> tuple[float, float]:
    """Return (allocated_MB, reserved_MB) on GPU 0."""
    if torch.cuda.is_available():
        alloc = torch.cuda.memory_allocated(0) / 1024**2
        reserv = torch.cuda.memory_reserved(0) / 1024**2
        return alloc, reserv
    return 0.0, 0.0


def find_latest_checkpoint(checkpoint_dir: str) -> str | None:
    """Find the most recent checkpoint file by step number."""
    if not os.path.exists(checkpoint_dir):
        return None
    ckpts = [f for f in os.listdir(checkpoint_dir) if f.startswith("ckpt_step") and f.endswith(".pt")]
    if not ckpts:
        return None
    # Extract step numbers and find the max
    def step_num(fname):
        m = re.search(r"ckpt_step(\d+)", fname)
        return int(m.group(1)) if m else 0
    latest = max(ckpts, key=step_num)
    return os.path.join(checkpoint_dir, latest)


def load_loss_history(log_path: str, up_to_step: int):
    """Reload train/val losses from the JSONL log for loss curve continuity."""
    train_losses, val_losses, logged_steps = [], [], []
    if not os.path.exists(log_path):
        return train_losses, val_losses, logged_steps
    with open(log_path, "r") as f:
        for line in f:
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            s = rec.get("step", 0)
            if s > up_to_step:
                continue
            if "train_loss" in rec:
                train_losses.append(rec["train_loss"])
                logged_steps.append(s)
            if "val_loss" in rec:
                val_losses.append(rec["val_loss"])
    return train_losses, val_losses, logged_steps


def evaluate(model, val_loader, device, max_batches=50):
    """Compute average validation loss over max_batches batches."""
    model.eval()
    total_loss = 0.0
    count = 0
    with torch.no_grad():
        for x, y in val_loader:
            if count >= max_batches:
                break
            x, y = x.to(device), y.to(device)
            with torch.autocast(device_type="cuda", dtype=torch.bfloat16, enabled=tcfg.use_bf16):
                _, loss = model(x, y)
            total_loss += loss.item()
            count += 1
    model.train()
    return total_loss / max(count, 1)


@torch.no_grad()
def generate_sample(model, device):
    """Generate a sample text continuation from the configured prompt."""
    model.eval()
    tok = get_tokenizer()
    prompt_ids = encode(tcfg.gen_prompt)
    idx = torch.tensor([prompt_ids], dtype=torch.long, device=device)
    out = model.generate(
        idx,
        max_new_tokens=tcfg.gen_max_new_tokens,
        temperature=tcfg.gen_temperature,
        top_k=tcfg.gen_top_k
    )
    text = decode(out[0].tolist())
    model.train()
    return text


def main():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    if device.type == "cuda":
        torch.cuda.empty_cache()

    # ── Update vocab size from tokenizer ─────────────────────────────────────
    tok = get_tokenizer()
    mcfg.vocab_size = tok.vocab_size

    # ── Build model ───────────────────────────────────────────────────────────
    model = NanoLLM(mcfg).to(device)
    n_params = model.count_parameters()

    # ── Optimizer ─────────────────────────────────────────────────────────────
    # Separate weight decay: don't apply to biases, norms, embeddings
    decay_params     = [p for n, p in model.named_parameters() if p.dim() >= 2]
    no_decay_params  = [p for n, p in model.named_parameters() if p.dim() < 2]
    optim_groups = [
        {"params": decay_params,    "weight_decay": tcfg.weight_decay},
        {"params": no_decay_params, "weight_decay": 0.0},
    ]
    optimizer = torch.optim.AdamW(optim_groups, lr=tcfg.learning_rate, betas=(0.9, 0.95), fused=True)

    # ── Resume from checkpoint (if available) ─────────────────────────────────
    resume_step = 0
    ckpt_path = find_latest_checkpoint(tcfg.checkpoint_dir)
    if ckpt_path:
        ckpt = torch.load(ckpt_path, map_location=device, weights_only=True)
        model.load_state_dict(ckpt["model_state"])
        optimizer.load_state_dict(ckpt["optimizer_state"])
        resume_step = ckpt["step"]
        print(f"  ✓ Resuming from checkpoint: {os.path.basename(ckpt_path)} (step {resume_step})")
        del ckpt  # Free memory
        if device.type == "cuda":
            torch.cuda.empty_cache()

    # ── Data ──────────────────────────────────────────────────────────────────
    train_loader, val_loader = get_dataloaders()
    train_iter = iter(train_loader)

    # ── Logging setup ─────────────────────────────────────────────────────────
    os.makedirs(tcfg.log_dir, exist_ok=True)
    log_path = os.path.join(tcfg.log_dir, "train_log.jsonl")

    # Reload prior loss history for complete loss curve
    if resume_step > 0:
        train_losses, val_losses, logged_steps = load_loss_history(log_path, resume_step)
        print(f"  ✓ Loaded {len(train_losses)} train / {len(val_losses)} val loss records from log")
    else:
        train_losses, val_losses, logged_steps = [], [], []

    # ── Derived constants ─────────────────────────────────────────────────────
    effective_batch = tcfg.batch_size * tcfg.grad_accum_steps
    tokens_per_step = effective_batch * mcfg.max_seq_len

    # ── Startup banner ────────────────────────────────────────────────────────
    gpu_name = torch.cuda.get_device_name(0) if device.type == "cuda" else "N/A"
    gpu_mem_total = torch.cuda.get_device_properties(0).total_memory / 1024**3 if device.type == "cuda" else 0

    print()
    print("=" * 62)
    print("  NanoLLM — Training Run")
    print("=" * 62)
    print(f"  Device          : {device} ({gpu_name})")
    print(f"  GPU Memory      : {gpu_mem_total:.1f} GB")
    print(f"  Parameters      : {n_params:,}  (~{n_params/1e6:.1f}M)")
    print(f"  Vocab size      : {mcfg.vocab_size:,}")
    print(f"  Context length  : {mcfg.max_seq_len}")
    print(f"  Layers / Heads  : {mcfg.num_layers}L / {mcfg.num_heads}H  (d={mcfg.embed_dim})")
    print(f"  Precision       : {'bf16' if tcfg.use_bf16 else 'fp32'}")
    print("-" * 62)
    print(f"  Micro-batch     : {tcfg.batch_size}")
    print(f"  Grad accum      : {tcfg.grad_accum_steps}")
    print(f"  Effective batch : {effective_batch}")
    print(f"  Tokens / step   : {tokens_per_step:,}")
    print(f"  Total steps     : {tcfg.max_steps:,}")
    print(f"  LR              : {tcfg.learning_rate}  (warmup {tcfg.warmup_steps} steps)")
    print(f"  Weight decay    : {tcfg.weight_decay}")
    print(f"  Grad clip       : {tcfg.grad_clip}")
    print("-" * 62)
    print(f"  Eval every      : {tcfg.eval_interval} steps")
    print(f"  Save every      : {tcfg.save_interval} steps")
    print(f"  Log every       : {tcfg.log_interval} steps")
    if resume_step > 0:
        print(f"  Resuming from   : step {resume_step}")
        print(f"  Remaining steps : {tcfg.max_steps - resume_step:,}")
    print("=" * 62)
    print()

    # ── Training loop ─────────────────────────────────────────────────────────
    model.train()
    step = resume_step
    optimizer.zero_grad()
    train_start = time.time()
    t0 = time.time()

    while step < tcfg.max_steps:

        # ── LR schedule ───────────────────────────────────────────────────────
        lr_mult = cosine_lr_with_warmup(step, tcfg)
        current_lr = tcfg.learning_rate * lr_mult
        for g in optimizer.param_groups:
            g["lr"] = current_lr

        # ── Gradient accumulation ─────────────────────────────────────────────
        accum_loss = 0.0
        for micro_step in range(tcfg.grad_accum_steps):
            try:
                x, y = next(train_iter)
            except StopIteration:
                train_iter = iter(train_loader)
                x, y = next(train_iter)

            x, y = x.to(device), y.to(device)

            with torch.autocast(device_type="cuda", dtype=torch.bfloat16, enabled=tcfg.use_bf16):
                _, loss = model(x, y)
                loss = loss / tcfg.grad_accum_steps  # Normalize gradient

            loss.backward()
            accum_loss += loss.item()

        # ── Gradient clip + optimizer step ────────────────────────────────────
        torch.nn.utils.clip_grad_norm_(model.parameters(), tcfg.grad_clip)
        optimizer.step()
        optimizer.zero_grad()

        step += 1
        train_losses.append(accum_loss)
        logged_steps.append(step)

        # ── Logging ───────────────────────────────────────────────────────────
        if step % tcfg.log_interval == 0:
            t1 = time.time()
            dt = (t1 - t0) / tcfg.log_interval
            t0 = t1

            elapsed = t1 - train_start
            remaining = dt * (tcfg.max_steps - step)
            toks_per_sec = tokens_per_step / dt if dt > 0 else 0
            progress_pct = step / tcfg.max_steps * 100

            alloc_mb, reserv_mb = get_gpu_mem_mb()

            print(
                f"  step {step:>6}/{tcfg.max_steps}"
                f"  ({progress_pct:4.1f}%)"
                f"  │ loss {accum_loss:.4f}"
                f"  │ lr {current_lr:.2e}"
                f"  │ {dt*1000:.0f}ms/step"
                f"  │ {toks_per_sec/1000:.1f}k tok/s"
                f"  │ GPU {alloc_mb:.0f}/{gpu_mem_total*1024:.0f}MB"
                f"  │ elapsed {format_time(elapsed)}"
                f"  │ ETA {format_time(remaining)}"
            )
            log_to_jsonl(log_path, {
                "step": step, "train_loss": accum_loss, "lr": current_lr,
                "ms_per_step": dt * 1000, "tokens_per_sec": toks_per_sec,
                "gpu_alloc_mb": alloc_mb,
            })

        # ── Evaluation ────────────────────────────────────────────────────────
        if step % tcfg.eval_interval == 0:
            val_loss = evaluate(model, val_loader, device)
            val_losses.append(val_loss)
            ppl = torch.exp(torch.tensor(val_loss)).item()
            sample = generate_sample(model, device)

            print()
            print(f"  ┌{'─' * 58}┐")
            print(f"  │  EVAL @ step {step:<6}                                    │")
            print(f"  │  Val Loss : {val_loss:.4f}   Perplexity : {ppl:<10.2f}          │")
            print(f"  ├{'─' * 58}┤")
            print(f"  │  Sample: {sample[:46]:<48}│")
            # Print remaining sample in wrapped lines if needed
            remaining_text = sample[46:200]
            while remaining_text:
                chunk = remaining_text[:48]
                remaining_text = remaining_text[48:]
                print(f"  │          {chunk:<48}│")
            print(f"  └{'─' * 58}┘")
            print()

            log_to_jsonl(log_path, {"step": step, "val_loss": val_loss, "perplexity": ppl})

        # ── Checkpoint ────────────────────────────────────────────────────────
        if step % tcfg.save_interval == 0:
            save_checkpoint(model, optimizer, step, accum_loss, tcfg)

    # ── Save final checkpoint and loss curve ──────────────────────────────────
    total_time = time.time() - train_start
    save_checkpoint(model, optimizer, step, accum_loss, tcfg)
    plot_loss_curve(
        train_losses, val_losses, logged_steps,
        save_path=os.path.join(tcfg.log_dir, "loss_curve.png")
    )

    print()
    print("=" * 62)
    print("  Training Complete!")
    print("=" * 62)
    print(f"  Total time      : {format_time(total_time)}")
    print(f"  Final val loss  : {val_losses[-1]:.4f}")
    print(f"  Final perplexity: {torch.exp(torch.tensor(val_losses[-1])):.2f}")
    print(f"  Steps completed : {step:,}")
    print(f"  Tokens processed: {step * tokens_per_step:,}")
    print("=" * 62)
    print()


if __name__ == "__main__":
    main()

