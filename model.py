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

def precompute_rope_freqs(head_dim: int, max_seq_len: int, theta: float = 10000.0) -> torch.Tensor:
    freqs = 1.0 / (theta ** (torch.arange(0, head_dim, 2).float() / head_dim))
    t = torch.arange(max_seq_len)
    freqs = torch.outer(t, freqs)
    return torch.polar(torch.ones_like(freqs), freqs)

def apply_rope(x: torch.Tensor, freqs: torch.Tensor) -> torch.Tensor:
    B, H, T, D = x.shape
    x_complex = torch.view_as_complex(x.float().reshape(B, H, T, D // 2, 2))
    freqs = freqs[:T].unsqueeze(0).unsqueeze(0)
    x_rotated = x_complex * freqs
    return torch.view_as_real(x_rotated).reshape(B, H, T, D).type_as(x)

class CausalSelfAttention(nn.Module):
    def __init__(self, cfg: ModelConfig):
        super().__init__()
        assert cfg.embed_dim % cfg.num_heads == 0
        self.num_heads = cfg.num_heads
        self.head_dim = cfg.embed_dim // cfg.num_heads
        self.dropout = cfg.dropout

        self.qkv = nn.Linear(cfg.embed_dim, 3 * cfg.embed_dim, bias=False)
        self.out_proj = nn.Linear(cfg.embed_dim, cfg.embed_dim, bias=False)
        self.attn_dropout = nn.Dropout(cfg.dropout)

    def forward(self, x: torch.Tensor, freqs: torch.Tensor) -> torch.Tensor:
        B, T, D = x.shape
        q, k, v = self.qkv(x).split(D, dim=2)
        
        def reshape(t):
            return t.view(B, T, self.num_heads, self.head_dim).transpose(1, 2)
            
        q, k, v = reshape(q), reshape(k), reshape(v)
        
        q = apply_rope(q, freqs)
        k = apply_rope(k, freqs)
        
        dropout_p = self.dropout if self.training else 0.0
        attn_out = F.scaled_dot_product_attention(q, k, v, dropout_p=dropout_p, is_causal=True)
        attn_out = attn_out.transpose(1, 2).contiguous().view(B, T, D)
        return self.out_proj(attn_out)

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

    def forward(self, x, freqs):
        x = x + self.dropout(self.attn(self.ln_1(x), freqs))
        x = x + self.dropout(self.mlp(self.ln_2(x)))
        return x

class MiniLLM(nn.Module):
    def __init__(self, cfg: ModelConfig):
        super().__init__()
        self.cfg = cfg
        self.token_embed = nn.Embedding(cfg.vocab_size, cfg.embed_dim)
        self.embed_dropout = nn.Dropout(cfg.dropout)
        self.blocks = nn.ModuleList([TransformerBlock(cfg) for _ in range(cfg.num_layers)])
        self.norm_final = RMSNorm(cfg.embed_dim)
        self.lm_head = nn.Linear(cfg.embed_dim, cfg.vocab_size, bias=False)
        self.lm_head.weight = self.token_embed.weight
        
        freqs = precompute_rope_freqs(cfg.embed_dim // cfg.num_heads, cfg.max_seq_len)
        self.register_buffer("rope_freqs", freqs)

    def forward(self, idx, targets=None):
        B, T = idx.size()
        
        x = self.embed_dropout(self.token_embed(idx))
        
        for block in self.blocks:
            x = block(x, self.rope_freqs)
            
        x = self.norm_final(x)
        logits = self.lm_head(x)
        
        loss = None
        if targets is not None:
            loss = F.cross_entropy(logits.view(-1, logits.size(-1)), targets.view(-1))
            
        return logits, loss
