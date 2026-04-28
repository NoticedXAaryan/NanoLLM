# train.py
# Simple training loop.

import torch
from config import model_config as mcfg, train_config as tcfg
from model import MiniLLM
from data import get_dataloaders
from tokenizer import get_tokenizer
from utils import save_checkpoint

def main():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"[train] Using device: {device}")

    tok = get_tokenizer()
    mcfg.vocab_size = tok.vocab_size

    model = MiniLLM(mcfg).to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=tcfg.learning_rate)

    train_loader, _ = get_dataloaders()
    train_iter = iter(train_loader)

    model.train()
    step = 0

    print(f"[train] Starting training for {tcfg.max_steps} steps...")
    
    while step < tcfg.max_steps:
        try:
            x, y = next(train_iter)
        except StopIteration:
            train_iter = iter(train_loader)
            x, y = next(train_iter)

        x, y = x.to(device), y.to(device)

        optimizer.zero_grad()
        _, loss = model(x, y)
        loss.backward()
        optimizer.step()

        step += 1

        if step % 50 == 0:
            print(f"[step {step}] loss={loss.item():.4f}")

        if step % 2000 == 0:
            save_checkpoint(model, optimizer, step, loss.item(), tcfg)

if __name__ == "__main__":
    main()
