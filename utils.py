# utils.py
# Simple utilities for saving checkpoints.

import os
import torch
from config import TrainConfig

def save_checkpoint(model, optimizer, step: int, loss: float, cfg: TrainConfig):
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
    ckpt = torch.load(path, map_location=device)
    model.load_state_dict(ckpt["model_state"])
    optimizer.load_state_dict(ckpt["optimizer_state"])
    print(f"[ckpt] Loaded checkpoint from step {ckpt['step']}")
    return ckpt["step"]
