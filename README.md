# 🧠 NanoLLM

NanoLLM is a from-scratch, educational implementation of a ~30M parameter language model. Rather than cloning older architectures like GPT-2, NanoLLM is built with the same modern architectural choices powering today's state-of-the-art models (like LLaMA 3 and Mistral), including RoPE, RMSNorm, and SwiGLU activations. It is designed to be highly readable, fully reproducible, and optimized to train efficiently on a single consumer GPU (8GB VRAM).

---

## ✨ Architecture

This is **not** a GPT-2 clone. NanoLLM uses the same architectural improvements found in LLaMA, Mistral, and Gemma:

| Component | Choice | Why |
|---|---|---|
| Positional Embedding | **RoPE** | Relative, generalizes to longer sequences |
| Normalization | **RMSNorm** | Simpler, faster than LayerNorm |
| Activation | **SwiGLU** | Better gradient flow than GELU |
| Attention | **Causal multi-head** with Flash Attention | Efficient O(n) memory |
| Weight tying | Embed ↔ LM head | Fewer params, better training |

### Model Size

| Hyperparameter | Value |
|---|---|
| Parameters | ~30M |
| Layers | 6 |
| Attention heads | 6 |
| Embedding dim | 384 |
| Context length | 256 tokens |
| Vocabulary | 50,257 (GPT-2 BPE) |

---

## 📊 Training

- **Dataset:** [TinyStories](https://huggingface.co/datasets/roneneldan/TinyStories) — 2.1M short stories
- **Hardware:** NVIDIA RTX 4060 Ti 8GB
- **Precision:** bf16 mixed precision
- **Effective batch size:** 256 (64 × 4 grad accum steps)
- **LR schedule:** Cosine decay with warmup
- **Steps:** 20,000 (~2–3 hours)

![Loss Curve](logs/loss_curve.png)

---

## 🚀 Quickstart

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Train
```bash
python train.py
```
Data is downloaded and tokenized automatically on first run.

### 3. Generate text
```bash
python generate.py \
  --checkpoint checkpoints/ckpt_step20000.pt \
  --prompt "Once upon a time there was a little girl" \
  --max_new_tokens 200
```

---

## 📝 Sample Outputs

After ~20,000 steps, the model generates coherent short stories:

```
Prompt: Once upon a time

Once upon a time, there was a little rabbit named Benny who lived in a
cozy burrow under an old oak tree. One day, Benny found a shiny red
apple near the meadow. He wanted to bring it home for his mother, but
it was very heavy. He pushed and pushed until finally...
```

---

## 📁 Project Structure

```
NanoLLM/
├── config.py       # All hyperparameters in one place
├── model.py        # LLaMA-style transformer architecture
├── data.py         # TinyStories download + tokenization
├── train.py        # Training loop
├── generate.py     # Text generation script
├── tokenizer.py    # GPT-2 BPE tokenizer wrapper
├── utils.py        # LR schedule, checkpointing, plotting
└── README.md
```

---

## 🧪 Key Training Details

- **bf16 mixed precision** — fits larger batches in 8GB VRAM without quality loss
- **Gradient accumulation** — simulates 256-sample batches using 64-sample physical batches
- **Cosine LR with warmup** — standard schedule for LLM pre-training
- **Gradient clipping (norm=1.0)** — prevents training instability
- **Decoupled weight decay** (no decay on biases/norms) — AdamW best practice
- **Residual projection scaling** — output projections initialized to `1/sqrt(2*layers)` for stable deep network training

---

## 📜 License

MIT — use freely, credit appreciated.
