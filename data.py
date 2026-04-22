# data.py
# Basic data loading without caching yet.

import torch
from torch.utils.data import Dataset, DataLoader
from datasets import load_dataset
from tokenizer import get_tokenizer, encode
from config import train_config as tcfg, model_config as mcfg

class SimpleTokenDataset(Dataset):
    def __init__(self, split="train", max_samples=10000):
        print(f"[data] Loading dataset split: {split}")
        dataset = load_dataset(tcfg.dataset_name, split=split)
        
        self.samples = []
        count = 0
        for example in dataset:
            if count >= max_samples:
                break
            tokens = encode(example["text"])
            if len(tokens) >= mcfg.max_seq_len + 1:
                self.samples.append(tokens[:mcfg.max_seq_len + 1])
                count += 1

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        chunk = self.samples[idx]
        x = torch.tensor(chunk[:-1], dtype=torch.long)
        y = torch.tensor(chunk[1:], dtype=torch.long)
        return x, y

def get_dataloaders():
    train_ds = SimpleTokenDataset("train", max_samples=20000)
    train_loader = DataLoader(train_ds, batch_size=tcfg.batch_size, shuffle=True)
    return train_loader, None
