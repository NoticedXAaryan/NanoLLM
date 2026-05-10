import json
import matplotlib.pyplot as plt
import os

# Set a beautiful, dark, modern developer aesthetic
plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(14, 7), dpi=300)
fig.patch.set_facecolor('#0d1117')
ax.set_facecolor('#0d1117')

log_path_1 = '../Training_Results/run_logs/run_001_train_log.jsonl'
log_path_2 = '../Training_Results/run_logs/run_002_train_log.jsonl'
output_path = '../assets/training_loss_curve.png'

steps = []
train_loss = []
val_steps = []
val_loss = []

# Load Run 1
if os.path.exists(log_path_1):
    with open(log_path_1, 'r') as f:
        for line in f:
            data = json.loads(line)
            if 'train_loss' in data:
                steps.append(data['step'])
                train_loss.append(data['train_loss'])
            if 'val_loss' in data:
                val_steps.append(data['step'])
                val_loss.append(data['val_loss'])

# Load Run 2
if os.path.exists(log_path_2):
    with open(log_path_2, 'r') as f:
        for line in f:
            data = json.loads(line)
            if 'train_loss' in data and data['step'] not in steps:
                steps.append(data['step'])
                train_loss.append(data['train_loss'])
            if 'val_loss' in data and data['step'] not in val_steps:
                val_steps.append(data['step'])
                val_loss.append(data['val_loss'])

# Sort by step just in case
sorted_train = sorted(zip(steps, train_loss))
steps = [x[0] for x in sorted_train]
train_loss = [x[1] for x in sorted_train]

sorted_val = sorted(zip(val_steps, val_loss))
val_steps = [x[0] for x in sorted_val]
val_loss = [x[1] for x in sorted_val]

# Plot lines with neon aesthetics
ax.plot(steps, train_loss, color='#58a6ff', alpha=0.6, linewidth=1.5, label='Training Loss')
ax.plot(val_steps, val_loss, color='#ff7b72', marker='o', markersize=6, linewidth=2, label='Validation Loss')

# Annotate the VRAM swapping bottleneck
ax.axvline(x=17550, color='#f0883e', linestyle='--', alpha=0.8, ymin=0.1, ymax=0.9)
ax.annotate('System VRAM Bottleneck\n(Background Process Swapping)', 
            xy=(17550, 2.5), xytext=(11000, 3.0),
            color='#f0883e', fontsize=11, fontweight='bold',
            arrowprops=dict(facecolor='#f0883e', edgecolor='#f0883e', arrowstyle='->', lw=2))

# Annotate the resume point
ax.axvline(x=4000, color='#3fb950', linestyle=':', alpha=0.6, ymin=0.1, ymax=0.9)
ax.annotate('Resumed Training (Run 2)', 
            xy=(4000, 4.0), xytext=(5000, 4.5),
            color='#3fb950', fontsize=10,
            arrowprops=dict(facecolor='#3fb950', edgecolor='#3fb950', arrowstyle='->', lw=1))

# Annotate final validation loss
if val_steps:
    final_step = val_steps[-1]
    final_val = val_loss[-1]
    ax.annotate(f'Final Val Loss: {final_val:.3f}', 
                xy=(final_step, final_val), xytext=(final_step - 4000, final_val + 0.5),
                color='#ff7b72', fontsize=12, fontweight='bold',
                bbox=dict(boxstyle="round,pad=0.3", fc="#0d1117", ec="#ff7b72", lw=1),
                arrowprops=dict(facecolor='#ff7b72', edgecolor='#ff7b72', arrowstyle='->', lw=2))

# Formatting
ax.set_title('NanoLLM Training Trajectory (Steps 0 - 20,000)', color='white', fontsize=18, pad=20, fontweight='bold')
ax.set_xlabel('Training Steps', color='#8b949e', fontsize=14)
ax.set_ylabel('Cross-Entropy Loss', color='#8b949e', fontsize=14)

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_color('#30363d')
ax.spines['left'].set_color('#30363d')
ax.tick_params(colors='#8b949e', which='both', labelsize=12)
ax.grid(True, color='#21262d', linestyle='-', linewidth=0.5, alpha=0.5)

legend = ax.legend(loc='upper right', frameon=True, facecolor='#0d1117', edgecolor='#30363d', fontsize=12)
for text in legend.get_texts():
    text.set_color('white')

plt.tight_layout()
plt.savefig(output_path, bbox_inches='tight')
print(f"Unified graph successfully generated and saved to {output_path}")
