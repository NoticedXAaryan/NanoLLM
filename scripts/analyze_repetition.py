import matplotlib.pyplot as plt
import os
import re

plt.style.use('dark_background')

def analyze_file(filepath):
    # Read the file
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract just Sample 1
    sample = content.split('[Sample 1]')[1].split('[Sample 2]')[0]
    
    # Get words
    words = re.findall(r'\b\w+\b', sample.lower())
    
    # Calculate cumulative unique words
    unique_words = set()
    cumulative_unique = []
    for i, word in enumerate(words):
        unique_words.add(word)
        cumulative_unique.append(len(unique_words))
        
    return list(range(len(words))), cumulative_unique

# Analyze the three files
x_100, y_100 = analyze_file('scratch/out_100.txt')
x_1000, y_1000 = analyze_file('scratch/out_1000.txt')

# We'll also analyze the 5000 one, but it might be broken. Let's try.
try:
    x_5000, y_5000 = analyze_file('scratch/out_5000.txt')
except Exception as e:
    x_5000, y_5000 = [], []
    print(f"Failed to load 5000: {e}")

# Plotting
fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
fig.patch.set_facecolor('#0d1117')
ax.set_facecolor('#0d1117')

ax.plot(x_100, y_100, label='100 Tokens (Coherent)', color='#3fb950', linewidth=2.5)
ax.plot(x_1000, y_1000, label='1,000 Tokens (Repetition Loop)', color='#d29922', linewidth=2.5)
if x_5000:
    ax.plot(x_5000, y_5000, label='5,000 Tokens (Context Collapse)', color='#f85149', linewidth=2.5)

ax.set_title('Attention Decay: Cumulative Unique Words over Sequence Length', color='white', pad=20, fontsize=14, fontweight='bold')
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
