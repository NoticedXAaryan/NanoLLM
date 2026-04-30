# train.py
# Main training loop for MiniLLM.
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
import time
import torch
from config import model_config as mcfg, train_config as tcfg
from model import MiniLLM
from data import get_dataloaders
from tokenizer import get_tokenizer, encode, decode
from utils import cosine_lr_with_warmup, save_checkpoint, plot_loss_curve, log_to_jsonl


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
    print(f"[train] Using device: {device}")

    # ── Update vocab size from tokenizer ─────────────────────────────────────
    tok = get_tokenizer()
    mcfg.vocab_size = tok.vocab_size
    print(f"[train] Vocab size: {mcfg.vocab_size}")

    # ── Build model ───────────────────────────────────────────────────────────
    model = MiniLLM(mcfg).to(device)
    n_params = model.count_parameters()
    print(f"[train] Model parameters: {n_params:,}  (~{n_params/1e6:.1f}M)")

    # ── Optimizer ─────────────────────────────────────────────────────────────
    # Separate weight decay: don't apply to biases, norms, embeddings
    decay_params     = [p for n, p in model.named_parameters() if p.dim() >= 2]
    no_decay_params  = [p for n, p in model.named_parameters() if p.dim() < 2]
    optim_groups = [
        {"params": decay_params,    "weight_decay": tcfg.weight_decay},
        {"params": no_decay_params, "weight_decay": 0.0},
    ]
    optimizer = torch.optim.AdamW(optim_groups, lr=tcfg.learning_rate, betas=(0.9, 0.95), fused=True)

    # ── Data ──────────────────────────────────────────────────────────────────
    train_loader, val_loader = get_dataloaders()
    train_iter = iter(train_loader)

    # ── Logging setup ─────────────────────────────────────────────────────────
    os.makedirs(tcfg.log_dir, exist_ok=True)
    log_path = os.path.join(tcfg.log_dir, "train_log.jsonl")
    train_losses, val_losses, logged_steps = [], [], []

    # ── Training loop ─────────────────────────────────────────────────────────
    model.train()
    step = 0
    optimizer.zero_grad()
    t0 = time.time()

    print(f"[train] Starting training for {tcfg.max_steps} steps...")
    print(f"[train] Effective batch size: {tcfg.batch_size * tcfg.grad_accum_steps}")

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
            print(f"[step {step:>6}] loss={accum_loss:.4f}  lr={current_lr:.2e}  {dt*1000:.1f}ms/step")
            log_to_jsonl(log_path, {"step": step, "train_loss": accum_loss, "lr": current_lr})

        # ── Evaluation ────────────────────────────────────────────────────────
        if step % tcfg.eval_interval == 0:
            val_loss = evaluate(model, val_loader, device)
            val_losses.append(val_loss)
            print(f"\n{'='*60}")
            print(f"  Step {step} | Val Loss: {val_loss:.4f} | Perplexity: {torch.exp(torch.tensor(val_loss)):.2f}")
            sample = generate_sample(model, device)
            print(f"  Sample: {sample[:200]}")
            print(f"{'='*60}\n")
            log_to_jsonl(log_path, {"step": step, "val_loss": val_loss})

        # ── Checkpoint ────────────────────────────────────────────────────────
        if step % tcfg.save_interval == 0:
            save_checkpoint(model, optimizer, step, accum_loss, tcfg)

    # ── Save final checkpoint and loss curve ──────────────────────────────────
    save_checkpoint(model, optimizer, step, accum_loss, tcfg)
    plot_loss_curve(
        train_losses, val_losses, logged_steps,
        save_path=os.path.join(tcfg.log_dir, "loss_curve.png")
    )
    print(f"\n[train] Done! Final val loss: {val_losses[-1]:.4f}")


if __name__ == "__main__":
    main()
