import json
from pathlib import Path

def validate(json_file):
    with open(json_file) as f:
        data = json.load(f)
    print(f"Validated {len(data)} questions from {json_file}")
    return len(data) > 0
