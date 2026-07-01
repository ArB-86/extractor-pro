from pathlib import Path
import json

data_dir = Path('/home/jiitcah.05/nlp_research_module/extractor_pro/output/master_dataset')
print(f"{'Chapter':<25} | {'Questions':<10}")
print('-' * 40)

for f in sorted(data_dir.glob('*.json')):
    with open(f, 'r') as jf:
        try:
            count = len(json.load(jf))
            print(f"{f.stem:<25} | {count:<10}")
        except:
            continue
