# generate.py
# Inference script — generate text from a trained checkpoint.
#
# Usage:
#   python generate.py --prompt "Once upon a time" --max_new_tokens 80 --num_samples 1
#
#   python generate.py --checkpoint models/NanoLLM_20k_weights.pt \
#                      --prompt "Once upon a time" \
#                      --max_new_tokens 200 \
#                      --temperature 0.8 \
#                      --top_k 40

import os
import argparse
import torch
from config import model_config as mcfg
from model import NanoLLM, load_model_weights
from tokenizer import get_tokenizer, encode, decode


def main():
    parser = argparse.ArgumentParser(description="Generate text from NanoLLM checkpoint")
    parser.add_argument("--checkpoint", type=str, help="Path to .pt checkpoint file")
    parser.add_argument("--prompt",     type=str, default="Once upon a time")
    parser.add_argument("--max_new_tokens", type=int, default=200)
    parser.add_argument("--temperature",    type=float, default=0.8,
                        help="Sampling temperature. Values <= 0 use greedy decoding.")
    parser.add_argument("--top_k",          type=int, default=40)
    parser.add_argument("--num_samples",    type=int, default=3, help="Number of independent samples")
    args = parser.parse_args()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Load tokenizer and update vocab size
    tok = get_tokenizer()
    mcfg.vocab_size = tok.vocab_size

    # Look for the lightweight standalone model first
    default_standalone_ckpt = os.path.join("models", "NanoLLM_20k_weights.pt")
    default_training_ckpt = os.path.join("Training_Results", "checkpoints", "ckpt_step20000.pt")

    if args.checkpoint:
        ckpt_path = args.checkpoint
    elif os.path.exists(default_standalone_ckpt):
        ckpt_path = default_standalone_ckpt
    elif os.path.exists(default_training_ckpt):
        ckpt_path = default_training_ckpt
    else:
        print("Error: Could not find checkpoint. Please specify with --checkpoint")
        return

    print(f"Loading model from {ckpt_path}...")
    checkpoint = torch.load(ckpt_path, map_location=device, weights_only=True)

    # Handle both standalone weights and training checkpoints
    if isinstance(checkpoint, dict) and "model_state" in checkpoint:
        model_weights = checkpoint["model_state"]
    else:
        model_weights = checkpoint

    # Initialize model. RoPE is rebuilt here; the saved rope buffer is ignored.
    model = NanoLLM(mcfg).to(device)
    load_model_weights(model, model_weights)
    model.eval()

    # Encode prompt
    prompt_ids = encode(args.prompt)
    idx = torch.tensor([prompt_ids], dtype=torch.long, device=device)

    # Generate
    print(f"Prompt: {args.prompt}\n{'-'*50}")
    for i in range(args.num_samples):
        out = model.generate(
            idx.clone(),
            max_new_tokens=args.max_new_tokens,
            temperature=args.temperature,
            top_k=args.top_k
        )
        text = decode(out[0].tolist())
        print(f"\n[Sample {i+1}]\n{text}\n{'-'*50}")


if __name__ == "__main__":
    main()
