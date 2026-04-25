# model.py
# Refactoring towards LLaMA architecture.
# Uses RMSNorm and SwiGLU.

import math
import torch
import torch.nn as nn
import torch.nn.functional as F
from config import ModelConfig

class RMSNorm(nn.Module):
    def __init__(self, dim: int, eps: float = 1e-6):
        super().__init__()
        self.eps = eps
        self.weight = nn.Parameter(torch.ones(dim))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        norm = x * torch.rsqrt(x.pow(2).mean(-1, keepdim=True) + self.eps)
        return self.weight * norm

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

class SwiGLU(nn.Module):
    def __init__(self, cfg: ModelConfig):
        super().__init__()
        hidden = int(2 * (cfg.ffn_multiplier * cfg.embed_dim) / 3)
        hidden = ((hidden + 63) // 64) * 64
        self.w1 = nn.Linear(cfg.embed_dim, hidden, bias=False)
        self.w2 = nn.Linear(cfg.embed_dim, hidden, bias=False)
        self.w3 = nn.Linear(hidden, cfg.embed_dim, bias=False)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.w3(F.silu(self.w1(x)) * self.w2(x))

class TransformerBlock(nn.Module):
    def __init__(self, cfg: ModelConfig):
        super().__init__()
        self.ln_1 = RMSNorm(cfg.embed_dim)
        self.attn = CausalSelfAttention(cfg)
        self.ln_2 = RMSNorm(cfg.embed_dim)
        self.mlp = SwiGLU(cfg)
        self.dropout = nn.Dropout(cfg.dropout)

    def forward(self, x):
        x = x + self.dropout(self.attn(self.ln_1(x)))
        x = x + self.dropout(self.mlp(self.ln_2(x)))
        return x

class MiniLLM(nn.Module):
    def __init__(self, cfg: ModelConfig):
        super().__init__()
        self.cfg = cfg
        self.wte = nn.Embedding(cfg.vocab_size, cfg.embed_dim)
        self.wpe = nn.Embedding(cfg.max_seq_len, cfg.embed_dim)
        self.drop = nn.Dropout(cfg.dropout)
        self.blocks = nn.ModuleList([TransformerBlock(cfg) for _ in range(cfg.num_layers)])
        self.ln_f = RMSNorm(cfg.embed_dim)
        self.lm_head = nn.Linear(cfg.embed_dim, cfg.vocab_size, bias=False)
        self.lm_head.weight = self.wte.weight

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
