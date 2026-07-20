from __future__ import annotations

import json
from pathlib import Path

INPUT = Path("datasets")
OUTPUT = Path("datasets/merged")

def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    out_file = OUTPUT / "all_questions.jsonl"

    total = 0
    with out_file.open("w", encoding="utf-8") as fout:
        for jsonl in INPUT.rglob("master_dataset.jsonl"):
            with jsonl.open("r", encoding="utf-8") as fin:
                for line in fin:
                    fout.write(line)
                    total += 1

    print(f"Merged {total} questions into {out_file}")

if __name__ == "__main__":
    main()
