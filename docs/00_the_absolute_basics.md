# 🌱 The Absolute Basics: From Zero to Neural Networks

> *"Before we can run, we must learn to walk."*

[🏠 Main Menu](../README.md) | [Next: Architecture Explained ➡️](./01_architecture_explained.md)

---

If you have a basic understanding of Python, you can absolutely build a Large Language Model. But before we dive into the complex architecture of NanoLLM, we need to understand the fundamental building blocks of AI.

How does a computer read a word? How does it "learn"?

## 1. How Computers "Read" (Tokens & Embeddings)

Computers only understand numbers. If you feed a neural network the sentence **"The cat sat"**, it will instantly crash. We have to translate English into Math.

### Step 1: Tokenization
We use a **Tokenizer** (like a giant dictionary). It assigns a unique ID to every word or sub-word. 

| Word | Token ID |
|------|----------|
| "The" | `464` |
| "cat" | `3797` |
| "sat" | `3332` |

> [!TIP]
> **Sub-words?** If the tokenizer sees a word it doesn't know, like "NanoLLM", it might split it into three tokens: `[Nano, L, LM]`. This keeps the dictionary size small!

### Step 2: The Embedding Matrix
A Token ID is just a list of IDs. There is no "meaning" yet. Every single token ID looks up its own personal list of numbers (a **Vector**). 

In NanoLLM, this vector is 384 numbers long. These numbers define the "meaning" of the word in a geometric space! Words with similar meanings (like "cat" and "dog") will have mathematically similar vectors.

### Step 3: The Tensor
The sentence "The cat sat" is now a 3D grid of numbers:
`Batch Size (1) × Sequence Length (3) × Embedding Size (384)`

This grid of numbers is called a **Tensor**. It is now ready to enter the Neural Network!

<details>
<summary>🔬 <strong>Deep Dive: What exactly is a Tensor?</strong></summary>

A Tensor is simply a fancy mathematical word for an array of numbers.
*   **0D Tensor:** A scalar (a single number like `5`).
*   **1D Tensor:** A Vector (a list of numbers `[1, 2, 3]`).
*   **2D Tensor:** A Matrix (like an Excel spreadsheet).
*   **3D Tensor:** A Cube of numbers (this is what language models use!).

PyTorch is a Python library specifically designed to do super-fast math on these Tensors using your GPU. 

🎥 **Further Learning:** To truly understand how these vectors map "meaning" in geometric space, watch [Word Embeddings by 3Blue1Brown](https://www.youtube.com/watch?v=gQddtTkdG14).
</details>

---

## 2. How Computers "Learn" (Backpropagation)

Okay, so we fed our Tensor into the model. Now we want the model to predict the next word. But when we first create the model, its "brain" is full of completely random numbers (Weights). It will guess random garbage.

How do we teach it? We use **Backpropagation**.

### 1. The Forward Pass (Guessing)
We feed the model: `"The cat"`.
The model uses its random math to make a guess. It predicts the next word is: `"helicopter"`.

### 2. The Loss Function (Grading the Test)
We know the actual next word should have been `"sat"`. We use a mathematical function called **Cross-Entropy Loss**. It compares the guess ("helicopter") to the truth ("sat") and spits out a score. A high score (like `Loss: 8.5`) means the model was terribly wrong.

### 3. Backpropagation (Finding the Blame)
Here is the magic of Calculus. The computer works backwards through the entire neural network. It calculates a **Gradient** for every single parameter. A Gradient is simply a direction: *"If I increase this specific number by 0.01, will my Loss go up or down?"*

### 4. The Optimizer (Fixing the Brain)
Now we use an **Optimizer** (like AdamW). It looks at all the Gradients and says: *"Okay, to get closer to the word 'sat', we need to turn this weight down by 0.01, and turn that weight up by 0.05."* It updates the weights. The model has just "learned"!

<details>
<summary>🔬 <strong>Deep Dive: The Calculus of Backpropagation</strong></summary>

If you want to build AI from scratch, you cannot escape the **Chain Rule of Calculus**.

A neural network is just a giant composite mathematical function: $f(g(h(x)))$. 
To figure out how much a weight deep inside the network ($w_1$) contributed to the final error ($L$), we multiply the derivatives backwards from the output to the input.

**The Chain Rule unrolled:**
$$ \frac{\partial L}{\partial w_1} = \frac{\partial L}{\partial y} \cdot \frac{\partial y}{\partial h} \cdot \frac{\partial h}{\partial w_1} $$

When you call `loss.backward()` in PyTorch, it is automatically calculating these massive partial derivatives for all 12.6 million parameters in NanoLLM simultaneously!

🎥 **Further Learning:** 
1. Watch [What is Backpropagation really doing? by 3Blue1Brown](https://www.youtube.com/watch?v=Ilg3gGewQ5U).
2. Take [Neural Networks: Zero to Hero by Andrej Karpathy](https://karpathy.ai/zero-to-hero.html). It is the definitive guide to building this exact math in Python.
</details>

---

[🏠 Main Menu](../README.md) | [Next: Architecture Explained ➡️](./01_architecture_explained.md)
