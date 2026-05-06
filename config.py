# config.py
# Central configuration for the mini-LLM project.
# All hyperparameters live here. Import this in every other file.

from dataclasses import dataclass

@dataclass
class ModelConfig:
    # Architecture
    vocab_size: int = 4096          # Will be overwritten by tokenizer vocab size
    embed_dim: int = 384            # Embedding / hidden dimension
    num_heads: int = 6              # Attention heads (embed_dim must be divisible by num_heads)
    num_layers: int = 6             # Transformer blocks
    ffn_multiplier: int = 4         # FFN hidden = embed_dim * ffn_multiplier (SwiGLU uses 2/3 of this)
    max_seq_len: int = 256          # Context window
    dropout: float = 0.1

@dataclass
class TrainConfig:
    # Data
    dataset_name: str = "roneneldan/TinyStories"
    tokenizer_name: str = "gpt2"    # Used for BPE tokenization; vocab size will be reduced
    data_cache_dir: str = "./data_cache"

    # Training
    batch_size: int = 32            # Per-GPU micro-batch size (tuned for 8 GB VRAM)
    grad_accum_steps: int = 8       # Effective batch = batch_size * grad_accum_steps = 256
    max_steps: int = 20000          # Total optimizer steps (~2–3 hours on 4060 Ti)
    warmup_steps: int = 500
    learning_rate: float = 3e-4
    weight_decay: float = 0.1
    grad_clip: float = 1.0
    eval_interval: int = 500        # Evaluate every N steps
    save_interval: int = 2000       # Save checkpoint every N steps
    log_interval: int = 50

    # Precision
    use_bf16: bool = True           # bf16 is more stable than fp16 on Ampere+ GPUs

    # Paths
    checkpoint_dir: str = "./checkpoints"
    log_dir: str = "./logs"

    # Generation (for eval during training)
    gen_prompt: str = "Once upon a time"
    gen_max_new_tokens: int = 100
    gen_temperature: float = 0.8
    gen_top_k: int = 40

model_config = ModelConfig()
train_config = TrainConfig()
