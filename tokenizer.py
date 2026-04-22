# tokenizer.py
# Wraps GPT-2 BPE tokenizer from HuggingFace.

from transformers import GPT2TokenizerFast

_tokenizer = None

def get_tokenizer():
    global _tokenizer
    if _tokenizer is None:
        _tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")
        _tokenizer.pad_token = _tokenizer.eos_token
    return _tokenizer

def encode(text: str) -> list[int]:
    tok = get_tokenizer()
    return tok.encode(text, add_special_tokens=False)

def decode(ids: list[int]) -> str:
    tok = get_tokenizer()
    return tok.decode(ids, skip_special_tokens=True)

def vocab_size() -> int:
    return get_tokenizer().vocab_size
