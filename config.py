# config.py
# Simple configuration for initial project setup.

from dataclasses import dataclass

@dataclass
class ModelConfig:
    vocab_size: int = 50257
    embed_dim: int = 384
    num_heads: int = 6
    num_layers: int = 6
    ffn_multiplier: int = 4
    max_seq_len: int = 256
    dropout: float = 0.1

@dataclass
class TrainConfig:
    dataset_name: str = "roneneldan/TinyStories"
    batch_size: int = 64
    max_steps: int = 20000
    learning_rate: float = 3e-4
    checkpoint_dir: str = "./checkpoints"

model_config = ModelConfig()
train_config = TrainConfig()
