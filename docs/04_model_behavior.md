# 🧪 Model Behavior & Inference

> *"A model is only as smart as its context window."*

[⬅️ Previous: Build It Yourself](./03_build_it_yourself.md) | [🏠 Main Menu](../README.md)

---

Now that you know how the engine works, it's time to actually drive it. 

You can run the model right now without any complex setup. By default, NanoLLM is configured to automatically detect the lightweight `models/NanoLLM_20k_weights.pt` file and run inference immediately.

**To generate a story:**
```bash
python generate.py --prompt "Once upon a time, there was a little girl named Lily." --max_new_tokens 100
```

But how does a tiny 12.6M parameter model actually behave in the wild? What happens if you push it to its limits? Let's map out its behavior across different scenarios.

---

## 1. The Sweet Spot (100 - 200 Tokens)

At short lengths, the model is highly coherent. Because it was trained on **TinyStories**, its entire universe consists of 3-year-old vocabulary. It understands basic grammar, object permanence, and simple dialogue.

**Prompt:** *"Once upon a time, there was a little girl named Lily."*
**Length:** 100 Tokens
**Output:**
> *"Once upon a time, there was a little girl named Lily. She loved to play outside in the garden. One day, she saw a big, red ball. She wanted to play with it. Lily ran to the ball and picked it up. It was very heavy. 'Wow, this is a big ball!' she said. Suddenly, a dog came running. The dog barked and wagged its tail. Lily laughed and threw the ball to the dog."*

**Verdict:** Perfect coherence. The syntax is flawless, and it successfully maintains the narrative thread.

---

## 2. The Repetition Trap (1,000 Tokens)

What happens if we ask the model to generate a massive 1,000-word story? 
A 12M parameter model does not have enough "brain capacity" (parameters) to maintain a complex plot for that long. It suffers from what is called **Attention Decay**.

**Prompt:** *"A brave knight went into the dark cave."*
**Length:** 1,000 Tokens
**Output (Excerpt around token 400):**
> *"...The knight found the gold. He was very happy. He looked at the gold. The gold was shiny. The knight liked the shiny gold. He put the gold in his bag. The knight found the gold. He was very happy. He looked at the gold. The gold was shiny..."*

**Verdict:** The model falls into a **Repetition Loop**. Once it loses track of the overarching plot, the easiest mathematical path for the Transformer is to just predict the exact same sequence of words it just wrote, over and over again. 

<details>
<summary>🔬 <strong>Deep Dive: Preventing Repetition Loops</strong></summary>

How do you fix this? You use a **Repetition Penalty** or adjust the **Temperature**.

When `generate.py` calculates the probabilities for the next word, it ranks them.
*   **Temperature = 0.0:** The model *always* picks the #1 most mathematically likely word. This guarantees a repetition loop.
*   **Temperature = 0.8:** The model sometimes picks the #2 or #3 most likely word. This injects "creativity" and forces the model to break out of loops.
*   **Top-K / Top-P Sampling:** We restrict the model from picking incredibly stupid words (the bottom 90% of the dictionary) so it stays creative but grammatically correct.

In `generate.py`, you can experiment with this:
```bash
python generate.py --temperature 1.2
```
*(Warning: Too high of a temperature will result in absolute chaos!)*
</details>

---

## 3. Pushing the Context Limit (10,000 Tokens)

Every LLM has a **Maximum Context Window** (the amount of tokens it can hold in its short-term memory at once). NanoLLM was configured with `max_seq_len = 256` during training.

If you try to force the model to generate or read 10,000 tokens, you will hit a mathematical wall.

**Prompt:** *(A massive 5,000-word block of text)*
**Length:** 10,000 Tokens
**Output:**
> *"...tree blue run fast apple tree blue run..." [Gibberish]* or an immediate Python crash: `IndexError: index out of range in self`.

**Verdict:** The model breaks. Because we trained the **RoPE (Rotary Position Embeddings)** up to 256 positions, if you ask it to rotate a vector to position 5,000, it encounters angles it has never seen before. The math collapses, and the model outputs pure gibberish.

<details>
<summary>🔬 <strong>Deep Dive: Context Window Extrapolation</strong></summary>

Modern researchers have found ways to stretch a model's context window *without* retraining it from scratch. Techniques like **YaRN** or **NTK-Aware Scaled RoPE** essentially "squish" the rotation angles so that 10,000 tokens mathematically look like 256 tokens to the model.

If you wanted to upgrade NanoLLM to read entire books, you would need to implement RoPE scaling in `model.py`!
</details>

---

<div align="center">
  <p><strong>You have reached the end of the Rabbit Hole.</strong></p>
  <p>You now understand the architecture, the training constraints, and the inference behavior of a modern LLM.</p>
  <p><em>Now go build your own.</em></p>
</div>
