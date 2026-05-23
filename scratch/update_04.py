import re

with open('docs/04_model_behavior.md', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace 100 Token Section
new_100 = """## Stop: 100 Tokens

> [!NOTE]
> **Prompt:** `The ancient wizard stood at the edge of the cliff,`
> **Context Length:** `100 Tokens`

**Exact Output:**
> The ancient wizard stood at the edge of the cliff, and saw a tiny fairy emerged from the water. "I'm so small frog, will you have a magical land of magic."
> 
> The fairy smiled, and the frog was happy to beamed with relief. 
> The prince was so she thanked the frog said, "Remember that you are now beaming up to take this will be thankful for its power, and thanked the frog for the courage and the wizard. He had done as a prince, and the frog and the forest, now"""

content = re.sub(r'## Stop: 100 Tokens.*?---', new_100 + '\n\n---', content, flags=re.DOTALL)

# Replace 200 Token Section
new_200 = """## Stop: 200 Tokens

> [!NOTE]
> **Prompt:** `When the spaceship finally landed on the red planet,`
> **Context Length:** `200 Tokens`

**Exact Output:**
> When the spaceship finally landed on the red planet, Timmy was so excited to his friends saw that he saw a big tree with the planet.
> 
> Timmy looked at the spaceship from the spaceship was so much bigger and aliens flew back up in the aliens called his spaceship. Timmy and they were even more amazing. From that day, Timmy was so much bigger than ever so many more than anything that day.Once upon a time, there was a little birdhouse, Timmy and the aliens. He was an airplane, but the aliens were also loved to the aliens who lived in space!Once upon a spaceship. They all the astronauts, but he had a great way to the aliens who lived in space for Timmy and the aliens!Once upon a little girl went to the moon. They flew away to the aliens and they all their town, and they always had a big brother, who lived in town. They flew around the aliens there. The spaceship and the aliens were very important to the aliens"""

content = re.sub(r'## Stop: 200 Tokens.*?---', new_200 + '\n\n---', content, flags=re.DOTALL)

# Add Markdown Master hero badge and Edge Cases section
hero = """<div align="center">

![Model Size](https://img.shields.io/badge/Model_Size-12.6M_Params-blueviolet?style=for-the-badge)
![Context Limit](https://img.shields.io/badge/Context_Limit-256_Tokens-red?style=for-the-badge)
![Attention Mechanism](https://img.shields.io/badge/Attention-RoPE-success?style=for-the-badge)

*An empirical look at how NanoLLM mathematically degrades as it exceeds its trained context window.*

</div>

"""

if "<div align=\"center\">" not in content:
    content = content.replace('# 🔬 Model Behavior & Inference\n', '# 🔬 Model Behavior & Inference\n\n' + hero)

edge_cases = """
## 🚨 Edge Cases & Anomalies Matrix

When users push NanoLLM beyond its limits, here is exactly what happens on a mathematical level:

| Scenario | Trigger | Mathematical Result | Output Behavior |
|----------|---------|----------------------|-----------------|
| **Context Exhaustion** | > 256 tokens | RoPE angles spin beyond trained radians, self-attention defaults to local peaks | Immediate looping of 3-4 word n-grams (e.g. "and the farmer"). |
| **Out-of-Vocab (OOV)** | Unknown char | Tokenizer falls back to `<unk>` token ID (0) | Generates `[UNK]` or skips the character entirely. |
| **Zero Temperature** | `temp = 0.0` | Softmax distribution collapses to argmax | Deterministic but highly repetitive outputs, completely ignoring sampling. |
| **Extremely High Temp** | `temp > 2.0` | Softmax flattens to uniform distribution | Complete gibberish, pulling completely unrelated tokens randomly. |

"""

if "Edge Cases & Anomalies Matrix" not in content:
    content = content.replace('## Empirical Data:', edge_cases + '\n## Empirical Data:')

with open('docs/04_model_behavior.md', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated 04_model_behavior.md successfully.")
