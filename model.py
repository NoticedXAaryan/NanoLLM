# model.py
# LLaMA-style decoder-only transformer.
#
# Key differences from vanilla GPT-2:
#   - RMSNorm instead of LayerNorm
#   - RoPE instead of learned positional embeddings
#   - SwiGLU activation in FFN instead of GELU
#   - Weight tying between token embedding and output projection
#
# These are the same design choices used in LLaMA, Mistral, and Gemma.

import math
import torch
import torch.nn as nn
import torch.nn.functional as F
from config import ModelConfig


# ─── RMSNorm ────────────────────────────────────────────────────────────────

class RMSNorm(nn.Module):
    """Root Mean Square Layer Normalization (Zhang & Sennrich, 2019).
    Simpler and slightly faster than LayerNorm; no mean subtraction.
    """
    def __init__(self, dim: int, eps: float = 1e-6):
        super().__init__()
        self.eps = eps
        self.weight = nn.Parameter(torch.ones(dim))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        norm = x * torch.rsqrt(x.pow(2).mean(-1, keepdim=True) + self.eps)
        return self.weight * norm


# ─── Rotary Positional Embeddings ───────────────────────────────────────────

def precompute_rope_freqs(head_dim: int, max_seq_len: int, theta: float = 10000.0) -> torch.Tensor:
    """Precompute complex rotation frequencies for RoPE.
    Returns shape (max_seq_len, head_dim // 2) as complex numbers.
    """
    freqs = 1.0 / (theta ** (torch.arange(0, head_dim, 2).float() / head_dim))
    t = torch.arange(max_seq_len)
    freqs = torch.outer(t, freqs)            # (T, head_dim//2)
    return torch.polar(torch.ones_like(freqs), freqs)  # complex


def apply_rope(x: torch.Tensor, freqs: torch.Tensor) -> torch.Tensor:
    """Apply rotary embeddings to query or key tensor.
    x: (B, num_heads, T, head_dim)
    freqs: (T, head_dim // 2) complex
    """
    B, H, T, D = x.shape
    x_complex = torch.view_as_complex(x.float().reshape(B, H, T, D // 2, 2))
    freqs = freqs[:T].unsqueeze(0).unsqueeze(0)   # (1, 1, T, D//2)
    x_rotated = x_complex * freqs
    return torch.view_as_real(x_rotated).reshape(B, H, T, D).type_as(x)


# ─── SwiGLU Feed-Forward Network ────────────────────────────────────────────

class SwiGLU(nn.Module):
    """SwiGLU FFN: FFN_SwiGLU(x) = (Swish(W1*x) ⊙ W2*x) * W3
    Uses 2/3 of the normal FFN hidden size to keep parameter count similar.
    This is the same FFN used in LLaMA.
    """
    def __init__(self, dim: int, ffn_multiplier: int):
        super().__init__()
        hidden = int(2 * (ffn_multiplier * dim) / 3)
        # Round to nearest multiple of 64 for hardware efficiency
        hidden = ((hidden + 63) // 64) * 64
        self.w1 = nn.Linear(dim, hidden, bias=False)
        self.w2 = nn.Linear(dim, hidden, bias=False)
        self.w3 = nn.Linear(hidden, dim, bias=False)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.w3(F.silu(self.w1(x)) * self.w2(x))


# ─── Causal Self-Attention ───────────────────────────────────────────────────

class CausalSelfAttention(nn.Module):
    """Multi-head causal self-attention with RoPE.
    Uses PyTorch's scaled_dot_product_attention for Flash Attention support.
    """
    def __init__(self, cfg: ModelConfig):
        super().__init__()
        assert cfg.embed_dim % cfg.num_heads == 0
        self.num_heads = cfg.num_heads
        self.head_dim = cfg.embed_dim // cfg.num_heads
        self.dropout = cfg.dropout

        # Single projection for Q, K, V
        self.qkv = nn.Linear(cfg.embed_dim, 3 * cfg.embed_dim, bias=False)
        self.out_proj = nn.Linear(cfg.embed_dim, cfg.embed_dim, bias=False)
        self.attn_dropout = nn.Dropout(cfg.dropout)

    def forward(self, x: torch.Tensor, freqs: torch.Tensor) -> torch.Tensor:
        B, T, D = x.shape
        q, k, v = self.qkv(x).split(D, dim=2)

        def reshape(t):
            return t.view(B, T, self.num_heads, self.head_dim).transpose(1, 2)

        q, k, v = reshape(q), reshape(k), reshape(v)

        # Apply RoPE to Q and K
        q = apply_rope(q, freqs)
        k = apply_rope(k, freqs)

        # Flash Attention (causal mask handled by is_causal=True)
        dropout_p = self.dropout if self.training else 0.0
        attn_out = F.scaled_dot_product_attention(q, k, v, dropout_p=dropout_p, is_causal=True)

        attn_out = attn_out.transpose(1, 2).contiguous().view(B, T, D)
        return self.out_proj(attn_out)


# ─── Transformer Block ───────────────────────────────────────────────────────

class TransformerBlock(nn.Module):
    """Single transformer block: pre-norm attention + pre-norm FFN."""
    def __init__(self, cfg: ModelConfig):
        super().__init__()
        self.norm1 = RMSNorm(cfg.embed_dim)
        self.attn = CausalSelfAttention(cfg)
        self.norm2 = RMSNorm(cfg.embed_dim)
        self.ffn = SwiGLU(cfg.embed_dim, cfg.ffn_multiplier)
        self.dropout = nn.Dropout(cfg.dropout)

    def forward(self, x: torch.Tensor, freqs: torch.Tensor) -> torch.Tensor:
        # Pre-norm residual connections
        x = x + self.dropout(self.attn(self.norm1(x), freqs))
        x = x + self.dropout(self.ffn(self.norm2(x)))
        return x


# ─── Full Language Model ─────────────────────────────────────────────────────

class MiniLLM(nn.Module):
    """Decoder-only transformer language model.
    Architecture: Token Embed → N x TransformerBlock → RMSNorm → LM Head
    Weight tying: token embedding and LM head share the same weights.
    """
    def __init__(self, cfg: ModelConfig):
        super().__init__()
        self.cfg = cfg

        self.token_embed = nn.Embedding(cfg.vocab_size, cfg.embed_dim)
        self.embed_dropout = nn.Dropout(cfg.dropout)
        self.blocks = nn.ModuleList([TransformerBlock(cfg) for _ in range(cfg.num_layers)])
        self.norm_final = RMSNorm(cfg.embed_dim)
        self.lm_head = nn.Linear(cfg.embed_dim, cfg.vocab_size, bias=False)

        # Weight tying — saves ~20M params and improves training stability
        self.lm_head.weight = self.token_embed.weight

        # Precompute RoPE frequencies (not a parameter, just a buffer)
        freqs = precompute_rope_freqs(cfg.embed_dim // cfg.num_heads, cfg.max_seq_len)
        self.register_buffer("rope_freqs", freqs)

        # Initialize weights
        self.apply(self._init_weights)

        # Scale residual projections by 1/sqrt(2 * num_layers) (GPT-2 trick)
        for name, p in self.named_parameters():
            if "out_proj" in name or "w3" in name:
                nn.init.normal_(p, mean=0.0, std=0.02 / math.sqrt(2 * cfg.num_layers))

    def _init_weights(self, module):
        if isinstance(module, nn.Linear):
            nn.init.normal_(module.weight, mean=0.0, std=0.02)
            if module.bias is not None:
                nn.init.zeros_(module.bias)
        elif isinstance(module, nn.Embedding):
            nn.init.normal_(module.weight, mean=0.0, std=0.02)

    def forward(self, idx: torch.Tensor, targets: torch.Tensor = None):
        """
        idx:     (B, T) token indices
        targets: (B, T) shifted token indices for loss computation
        Returns logits (B, T, vocab_size) and optionally cross-entropy loss.
        """
        B, T = idx.shape
        assert T <= self.cfg.max_seq_len, f"Sequence length {T} exceeds max_seq_len {self.cfg.max_seq_len}"

        x = self.embed_dropout(self.token_embed(idx))

        for block in self.blocks:
            x = block(x, self.rope_freqs)

        x = self.norm_final(x)
        logits = self.lm_head(x)   # (B, T, vocab_size)

        loss = None
        if targets is not None:
            loss = F.cross_entropy(logits.view(-1, logits.size(-1)), targets.view(-1))

        return logits, loss

    def count_parameters(self) -> int:
        return sum(p.numel() for p in self.parameters() if p.requires_grad)

    @torch.no_grad()
    def generate(self, idx: torch.Tensor, max_new_tokens: int,
                 temperature: float = 1.0, top_k: int = None) -> torch.Tensor:
        """Autoregressive generation with temperature and top-k sampling."""
        for _ in range(max_new_tokens):
            # Crop to max context window
            idx_cond = idx if idx.size(1) <= self.cfg.max_seq_len else idx[:, -self.cfg.max_seq_len:]
            logits, _ = self(idx_cond)
            logits = logits[:, -1, :] / temperature   # (B, vocab_size)

            if top_k is not None:
                v, _ = torch.topk(logits, min(top_k, logits.size(-1)))
                logits[logits < v[:, [-1]]] = float('-inf')

            probs = F.softmax(logits, dim=-1)
            next_token = torch.multinomial(probs, num_samples=1)
            idx = torch.cat([idx, next_token], dim=1)

        return idx
