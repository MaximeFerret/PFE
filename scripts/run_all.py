import subprocess
from pathlib import Path

root = Path("./data/PANCREAS")

all_cases = sorted(root.glob("PANCREAS_*"))

# Missing cases
skip = {"PANCREAS_0025", "PANCREAS_0070"}

for case in all_cases:
    if case.name in skip:
        print(f"⏭️ Skipping missing case: {case.name}")
        continue

    print(f"🚀 Starting simulation: {case.name}")
    subprocess.run(["python", "simulate_pancreas.py", str(case)], check=True)
