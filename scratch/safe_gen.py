import subprocess

def gen(prompt, tokens, out_file):
    cmd = f'python generate.py --prompt "{prompt}" --max_new_tokens {tokens} --num_samples 1'
    print(f"Running: {cmd}")
    res = subprocess.check_output(cmd, shell=True, text=True, encoding='utf-8', errors='ignore')
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write(res)
    print(f"Saved to {out_file}")

gen("The ancient wizard stood at the edge of the cliff,", 100, "scratch/out_100_new.txt")
gen("When the spaceship finally landed on the red planet,", 200, "scratch/out_200_new.txt")
