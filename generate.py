# generate.py
# Inference script — generate text from a trained checkpoint.
#
# Usage:
#   python generate.py --checkpoint checkpoints/ckpt_step20000.pt \
#                      --prompt "Once upon a time" \
#                      --max_new_tokens 200 \
#                      --temperature 0.8 \
#                      --top_k 40

import argparse
import torch
from config import model_config as mcfg
from model import NanoLLM
from tokenizer import get_tokenizer, encode, decode


def main():
    parser = argparse.ArgumentParser(description="Generate text from NanoLLM checkpoint")
    parser.add_argument("--checkpoint", type=str, required=True,  help="Path to .pt checkpoint file")
    parser.add_argument("--prompt",     type=str, default="Once upon a time")
    parser.add_argument("--max_new_tokens", type=int, default=200)
    parser.add_argument("--temperature",    type=float, default=0.8)
    parser.add_argument("--top_k",          type=int, default=40)
    parser.add_argument("--num_samples",    type=int, default=3, help="Number of independent samples")
    args = parser.parse_args()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Load tokenizer and update vocab size
    tok = get_tokenizer()
    mcfg.vocab_size = tok.vocab_size

    # Load model
    model = NanoLLM(mcfg).to(device)
    ckpt = torch.load(args.checkpoint, map_location=device)
    model.load_state_dict(ckpt["model_state"])
    model.eval()
    print(f"Loaded checkpoint from step {ckpt['step']}  (loss={ckpt['loss']:.4f})\n")

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
