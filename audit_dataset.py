import json
from pathlib import Path
from collections import Counter

counts = Counter()
for f in Path('output/master_dataset').glob('*.json'):
    with open(f, 'r') as jf:
        data = json.load(jf)
        counts[f.stem] = len(data)

print(f"{'Chapter File':<30} | {'Questions':<10}")
print("-" * 45)
for ch, count in counts.items():
    print(f"{ch:<30} | {count:<10}")
