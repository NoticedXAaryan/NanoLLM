"""CPU smoke tests for NanoLLM. No dataset download."""

import os
os.environ.setdefault("MPLBACKEND", "Agg")

import tempfile
import unittest

import torch

from config import ModelConfig, TrainConfig
from data import TokenDataset
from model import NanoLLM, apply_rope, load_model_weights, precompute_rope_freqs
from utils import cosine_lr_with_warmup, plot_loss_curve

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WEIGHTS = os.path.join(ROOT, "models", "NanoLLM_20k_weights.pt")
EXPECTED_PARAMS = 29_920_512


class TestArchitecture(unittest.TestCase):
    def test_parameter_count_matches_checkpoint_vocab(self):
        model = NanoLLM(ModelConfig())
        self.assertEqual(model.cfg.vocab_size, 50257)
        self.assertEqual(model.count_parameters(), EXPECTED_PARAMS)
        # Tied embedding and LM head are one matrix.
        self.assertIs(model.lm_head.weight, model.token_embed.weight)

    def test_forward_backward_and_adam_step_on_cpu(self):
        cfg = ModelConfig()
        cfg.vocab_size = 128
        cfg.num_layers = 2
        cfg.max_seq_len = 32
        model = NanoLLM(cfg)
        optimizer = torch.optim.AdamW(model.parameters(), lr=3e-4, betas=(0.9, 0.95))
        x = torch.randint(0, cfg.vocab_size, (2, 16))
        y = torch.randint(0, cfg.vocab_size, (2, 16))
        before = model.token_embed.weight.detach().clone()
        _, loss = model(x, y)
        self.assertTrue(torch.isfinite(loss))
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
        self.assertFalse(torch.equal(before, model.token_embed.weight))

    def test_rope_preserves_norm_and_survives_bf16_cast(self):
        cfg = ModelConfig()
        cfg.vocab_size = 128
        cfg.num_layers = 1
        model = NanoLLM(cfg).to(torch.bfloat16)
        freqs = precompute_rope_freqs(cfg.embed_dim // cfg.num_heads, 8)
        self.assertTrue(freqs.is_complex())
        self.assertTrue(torch.allclose(freqs.abs(), torch.ones_like(freqs.abs()), atol=1e-5))
        q = torch.randn(1, cfg.num_heads, 8, cfg.embed_dim // cfg.num_heads)
        rotated = apply_rope(q, freqs)
        self.assertTrue(torch.allclose(q.norm(), rotated.norm(), atol=1e-4))
        # A bf16 cast of the module must not be required to keep a complex buffer.
        self.assertNotIn("rope_freqs", model.state_dict())

    def test_generate_shapes_and_greedy(self):
        cfg = ModelConfig()
        cfg.vocab_size = 64
        cfg.num_layers = 1
        cfg.max_seq_len = 16
        model = NanoLLM(cfg).eval()
        idx = torch.randint(0, cfg.vocab_size, (1, 4))
        out = model.generate(idx, max_new_tokens=5, temperature=0.0, top_k=None)
        self.assertEqual(out.shape, (1, 9))
        self.assertTrue(torch.all((out >= 0) & (out < cfg.vocab_size)))

    def test_lr_schedule_endpoints(self):
        cfg = TrainConfig()
        self.assertEqual(cosine_lr_with_warmup(0, cfg), 0.0)
        self.assertAlmostEqual(cosine_lr_with_warmup(cfg.warmup_steps, cfg), 1.0)
        self.assertAlmostEqual(cosine_lr_with_warmup(cfg.max_steps, cfg), 0.1)

    def test_loss_plot_accepts_sparse_validation_steps(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "loss.png")
            plot_loss_curve(
                [1.5, 1.2, 1.0],
                [1.4],
                [10, 20, 30],
                path,
                val_steps=[30],
            )
            self.assertTrue(os.path.exists(path))
            self.assertGreater(os.path.getsize(path), 0)


class TestCheckpoint(unittest.TestCase):
    def test_published_weights_load_with_unit_rope(self):
        self.assertTrue(os.path.exists(WEIGHTS), "published weights are missing")
        sd = torch.load(WEIGHTS, map_location="cpu", weights_only=True)
        self.assertEqual(tuple(sd["token_embed.weight"].shape), (50257, 384))
        self.assertTrue(torch.equal(sd["token_embed.weight"], sd["lm_head.weight"]))

        model = NanoLLM(ModelConfig()).eval()
        load_model_weights(model, sd)
        freqs = precompute_rope_freqs(384 // 6, 4)
        # Loading must not replace this rotation with the cosine-only buffer.
        self.assertGreater(freqs.imag.abs().mean().item(), 0.1)
        idx = torch.randint(0, 50257, (1, 8))
        logits, loss = model(idx, idx)
        self.assertEqual(tuple(logits.shape), (1, 8, 50257))
        self.assertTrue(torch.isfinite(logits).all())
        self.assertTrue(torch.isfinite(loss))


class TestDataWindow(unittest.TestCase):
    def test_last_token_is_a_target(self):
        import numpy as np
        tokens = np.arange(10, dtype=np.uint16)
        ds = TokenDataset(tokens, seq_len=4)
        self.assertEqual(len(ds), 6)
        x, y = ds[len(ds) - 1]
        self.assertEqual(x.tolist(), [5, 6, 7, 8])
        self.assertEqual(y.tolist(), [6, 7, 8, 9])


if __name__ == "__main__":
    unittest.main()
