import matplotlib.pyplot as plt
import os
import re

plt.style.use('dark_background')

stops = [100, 200, 250, 500, 750, 1000, 2500, 5000]

def analyze_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        sample = content.split('[Sample 1]')[1].split('[Sample 2]')[0]
        words = re.findall(r'\b\w+\b', sample.lower())
        unique_words = set()
        cumulative_unique = []
        for i, word in enumerate(words):
            unique_words.add(word)
            cumulative_unique.append(len(unique_words))
        return list(range(len(words))), cumulative_unique
    except Exception as e:
        print(f"Failed to load {filepath}: {e}")
        return [], []

fig, ax = plt.subplots(figsize=(12, 7), dpi=300)
fig.patch.set_facecolor('#0d1117')
ax.set_facecolor('#0d1117')

colors = ['#3fb950', '#2ea043', '#8957e5', '#a371f7', '#d29922', '#e3b341', '#f85149', '#ff7b72']

for idx, tokens in enumerate(stops):
    x, y = analyze_file(f'scratch/outputs/out_{tokens}.txt')
    if x:
        ax.plot(x, y, label=f'{tokens} Tokens', color=colors[idx % len(colors)], linewidth=2)

ax.set_title('Attention Decay: Cumulative Unique Words over 8 Data Points', color='white', pad=20, fontsize=14, fontweight='bold')
ax.set_xlabel('Words Generated', color='#8b949e', fontsize=12)
ax.set_ylabel('Total Unique Words Used', color='#8b949e', fontsize=12)

ax.spines['bottom'].set_color('#30363d')
ax.spines['top'].set_visible(False) 
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#30363d')

ax.tick_params(axis='x', colors='#8b949e')
ax.tick_params(axis='y', colors='#8b949e')

ax.grid(True, linestyle='--', alpha=0.2, color='#8b949e')
ax.legend(facecolor='#161b22', edgecolor='#30363d', labelcolor='white')

os.makedirs('assets', exist_ok=True)
plt.savefig('assets/attention_decay.png', bbox_inches='tight', facecolor=fig.get_facecolor())
print("Plot saved to assets/attention_decay.png")
