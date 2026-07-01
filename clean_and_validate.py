import json
from pathlib import Path
import re

def clean_text(text):
    # Remove noise patterns
    noise = [r"rough work", r"16/04/18", r"unit-", r"fig\.", r"answer", r"solution", r"page"]
    for n in noise:
        text = re.sub(n, '', text, flags=re.IGNORECASE)
    return text.strip()

out_dir = Path('output/master_dataset')
for f in out_dir.glob('*.json'):
    with open(f, 'r') as jf:
        qs = json.load(jf)
    
    # Filter only meaningful questions
    valid_qs = []
    for q in qs:
        # Quality Filter: Skip short noise blocks
        txt = clean_text(q.get('question', ''))
        if len(txt) > 20 and '?' in txt or 'find' in txt.lower():
            q['question'] = txt
            valid_qs.append(q)
    
    # Save cleaned
    with open(f, 'w') as jf:
        json.dump(valid_qs, jf, indent=4)
