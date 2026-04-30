# utils.py
# Utility functions: cosine LR scheduler, checkpoint saving/loading,
# loss curve plotting, and parameter counting.

import os
import math
import json
import torch
import matplotlib.pyplot as plt
from config import TrainConfig


def cosine_lr_with_warmup(step: int, cfg: TrainConfig) -> float:
    """Returns the learning rate multiplier for the current step.
    Linear warmup → cosine decay → minimum LR floor (10% of peak).
    """
    min_lr = cfg.learning_rate * 0.1

    # Warmup phase
    if step < cfg.warmup_steps:
        return step / cfg.warmup_steps

    # After training ends, return floor
    if step > cfg.max_steps:
        return min_lr / cfg.learning_rate

    # Cosine decay
    progress = (step - cfg.warmup_steps) / (cfg.max_steps - cfg.warmup_steps)
    cosine_val = 0.5 * (1 + math.cos(math.pi * progress))
    lr = min_lr + (cfg.learning_rate - min_lr) * cosine_val
    return lr / cfg.learning_rate


def save_checkpoint(model, optimizer, step: int, loss: float, cfg: TrainConfig):
    """Save model + optimizer state and config."""
    os.makedirs(cfg.checkpoint_dir, exist_ok=True)
    path = os.path.join(cfg.checkpoint_dir, f"ckpt_step{step}.pt")
    torch.save({
        "step": step,
        "model_state": model.state_dict(),
        "optimizer_state": optimizer.state_dict(),
        "loss": loss,
    }, path)
    print(f"[ckpt] Saved checkpoint: {path}")


def load_checkpoint(model, optimizer, path: str, device: torch.device):
    """Load checkpoint. Returns the step number."""
    ckpt = torch.load(path, map_location=device)
    model.load_state_dict(ckpt["model_state"])
    optimizer.load_state_dict(ckpt["optimizer_state"])
    print(f"[ckpt] Loaded checkpoint from step {ckpt['step']}, loss={ckpt['loss']:.4f}")
    return ckpt["step"]


def plot_loss_curve(train_losses: list, val_losses: list, steps: list, save_path: str):
    """Save a clean loss curve plot to disk."""
    plt.figure(figsize=(10, 5))
    plt.plot(steps, train_losses, label="Train Loss", linewidth=2, color="#4C72B0")
    if val_losses:
        val_steps = [s for i, s in enumerate(steps) if i < len(val_losses)]
        plt.plot(val_steps[:len(val_losses)], val_losses,
                 label="Val Loss", linewidth=2, color="#DD8452", linestyle="--")
    plt.xlabel("Step")
    plt.ylabel("Cross-Entropy Loss")
    plt.title("MiniLLM Training Loss")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(save_path, dpi=150)
    plt.close()
    print(f"[plot] Loss curve saved to {save_path}")


def log_to_jsonl(log_path: str, record: dict):
    """Append a JSON record to a .jsonl log file."""
    with open(log_path, "a") as f:
        f.write(json.dumps(record) + "\n")
