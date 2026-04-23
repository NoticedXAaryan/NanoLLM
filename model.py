# model.py
# Baseline GPT-2 style transformer (pre-LLaMA architecture).
# Uses LayerNorm, GELU, and absolute positional embeddings.

import math
import torch
import torch.nn as nn
import torch.nn.functional as F
from config import ModelConfig

class CausalSelfAttention(nn.Module):
    def __init__(self, cfg: ModelConfig):
        super().__init__()
        assert cfg.embed_dim % cfg.num_heads == 0
        self.c_attn = nn.Linear(cfg.embed_dim, 3 * cfg.embed_dim)
        self.c_proj = nn.Linear(cfg.embed_dim, cfg.embed_dim)
        self.attn_dropout = nn.Dropout(cfg.dropout)
        self.resid_dropout = nn.Dropout(cfg.dropout)
        self.num_heads = cfg.num_heads
        self.head_dim = cfg.embed_dim // cfg.num_heads

    def forward(self, x):
        B, T, D = x.size()
        qkv = self.c_attn(x)
        q, k, v = qkv.split(D, dim=2)
        
        q = q.view(B, T, self.num_heads, self.head_dim).transpose(1, 2)
        k = k.view(B, T, self.num_heads, self.head_dim).transpose(1, 2)
        v = v.view(B, T, self.num_heads, self.head_dim).transpose(1, 2)
        
        y = F.scaled_dot_product_attention(q, k, v, is_causal=True)
        y = y.transpose(1, 2).contiguous().view(B, T, D)
        return self.resid_dropout(self.c_proj(y))

class FeedForward(nn.Module):
    def __init__(self, cfg: ModelConfig):
        super().__init__()
        hidden = cfg.embed_dim * 4
        self.c_fc = nn.Linear(cfg.embed_dim, hidden)
        self.act = nn.GELU()
        self.c_proj = nn.Linear(hidden, cfg.embed_dim)
        self.dropout = nn.Dropout(cfg.dropout)
        
    def forward(self, x):
        return self.dropout(self.c_proj(self.act(self.c_fc(x))))

class TransformerBlock(nn.Module):
    def __init__(self, cfg: ModelConfig):
        super().__init__()
        self.ln_1 = nn.LayerNorm(cfg.embed_dim)
        self.attn = CausalSelfAttention(cfg)
        self.ln_2 = nn.LayerNorm(cfg.embed_dim)
        self.mlp = FeedForward(cfg)

    def forward(self, x):
        x = x + self.attn(self.ln_1(x))
        x = x + self.mlp(self.ln_2(x))
        return x

class MiniLLM(nn.Module):
    def __init__(self, cfg: ModelConfig):
        super().__init__()
        self.cfg = cfg
        self.wte = nn.Embedding(cfg.vocab_size, cfg.embed_dim)
        self.wpe = nn.Embedding(cfg.max_seq_len, cfg.embed_dim)
        self.drop = nn.Dropout(cfg.dropout)
        self.blocks = nn.ModuleList([TransformerBlock(cfg) for _ in range(cfg.num_layers)])
        self.ln_f = nn.LayerNorm(cfg.embed_dim)
        self.lm_head = nn.Linear(cfg.embed_dim, cfg.vocab_size, bias=False)

    def forward(self, idx, targets=None):
        B, T = idx.size()
        pos = torch.arange(0, T, dtype=torch.long, device=idx.device)
        
        x = self.wte(idx) + self.wpe(pos)
        x = self.drop(x)
        
        for block in self.blocks:
            x = block(x)
            
        x = self.ln_f(x)
        logits = self.lm_head(x)
        
        loss = None
        if targets is not None:
            loss = F.cross_entropy(logits.view(-1, logits.size(-1)), targets.view(-1))
            
        return logits, loss
