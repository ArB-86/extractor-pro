from pathlib import Path
import json

data_dir = Path('output/master_dataset')

print(f"{'Chapter':<25} | {'Questions':<10} | {'Status'}")
print('-' * 50)

for f in sorted(data_dir.glob('*.json')):
    try:
        with open(f, 'r') as jf:
            data = json.load(jf)
            # Handle both list [] and dictionary {"questions": []} formats
            count = len(data) if isinstance(data, list) else len(data.get('questions', []))
            print(f"{f.stem:<25} | {count:<10} | OK")
    except Exception as e:
        print(f"{f.stem:<25} | {'ERROR':<10} | {str(e)[:20]}")
