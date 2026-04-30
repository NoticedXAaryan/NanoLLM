# data.py
# Downloads TinyStories from HuggingFace, tokenizes it with GPT-2 BPE,
# and returns PyTorch DataLoaders for training and validation.

import os
import torch
import numpy as np
from torch.utils.data import Dataset, DataLoader
from datasets import load_dataset
from tqdm import tqdm
from tokenizer import get_tokenizer
from config import train_config as tcfg, model_config as mcfg


# ─── Tokenize and Cache ───────────────────────────────────────────────────────

def tokenize_dataset(split: str = "train") -> np.ndarray:
    """Tokenize TinyStories split and cache as a flat numpy array on disk.
    Returns the token array.
    """
    os.makedirs(tcfg.data_cache_dir, exist_ok=True)
    cache_path = os.path.join(tcfg.data_cache_dir, f"{split}.bin")

    if os.path.exists(cache_path):
        print(f"[data] Loading cached {split} tokens from {cache_path}")
        return np.memmap(cache_path, dtype=np.uint16, mode="r")

    print(f"[data] Tokenizing TinyStories ({split})...")
    tok = get_tokenizer()
    eos_id = tok.eos_token_id

    dataset = load_dataset(tcfg.dataset_name, split=split, trust_remote_code=True)

    all_tokens = []
    for example in tqdm(dataset, desc=f"Tokenizing {split}"):
        ids = tok.encode(example["text"], add_special_tokens=False)
        ids.append(eos_id)       # Separate stories with EOS
        all_tokens.extend(ids)

    arr = np.array(all_tokens, dtype=np.uint16)
    mm = np.memmap(cache_path, dtype=np.uint16, mode="w+", shape=(len(arr),))
    mm[:] = arr
    mm.flush()
    print(f"[data] Saved {len(arr):,} tokens to {cache_path}")
    return mm


# ─── Dataset ─────────────────────────────────────────────────────────────────

class TokenDataset(Dataset):
    """Slices a flat token array into overlapping (input, target) pairs.
    input  = tokens[i : i+seq_len]
    target = tokens[i+1 : i+seq_len+1]  (next-token prediction)
    """
    def __init__(self, tokens: np.ndarray, seq_len: int):
        self.tokens = tokens
        self.seq_len = seq_len
        self.n = len(tokens) - seq_len - 1

    def __len__(self):
        return self.n

    def __getitem__(self, idx):
        chunk = self.tokens[idx: idx + self.seq_len + 1]
        x = torch.from_numpy(chunk[:-1].astype(np.int64))
        y = torch.from_numpy(chunk[1:].astype(np.int64))
        return x, y


# ─── Public API ──────────────────────────────────────────────────────────────

def get_dataloaders(seq_len: int = None, batch_size: int = None):
    """Returns (train_loader, val_loader)."""
    if seq_len is None:
        seq_len = mcfg.max_seq_len
    if batch_size is None:
        batch_size = tcfg.batch_size

    train_tokens = tokenize_dataset("train")
    val_tokens   = tokenize_dataset("validation")

    train_ds = TokenDataset(train_tokens, seq_len)
    val_ds   = TokenDataset(val_tokens,   seq_len)

    train_loader = DataLoader(
        train_ds, batch_size=batch_size, shuffle=True,
        num_workers=4, pin_memory=True, drop_last=True
    )
    val_loader = DataLoader(
        val_ds, batch_size=batch_size, shuffle=False,
        num_workers=2, pin_memory=True, drop_last=True
    )

    print(f"[data] Train: {len(train_ds):,} samples | Val: {len(val_ds):,} samples")
    return train_loader, val_loader
