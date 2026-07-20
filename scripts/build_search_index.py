from __future__ import annotations

import json
from pathlib import Path
import pickle

INPUT = Path("datasets/merged/all_questions.jsonl")
OUTPUT = Path("datasets/search_index.pkl")

def main():
    if not INPUT.exists():
        raise FileNotFoundError(INPUT)

    index = []
    with INPUT.open("r", encoding="utf-8") as f:
        for line in f:
            q = json.loads(line)
            index.append({
                "question_text": q.get("question_text", ""),
                "chapter": q.get("chapter"),
                "question_number": q.get("question_number"),
                "source_page": q.get("source_page"),
                "answer": q.get("answer"),
            })

    with OUTPUT.open("wb") as f:
        pickle.dump(index, f)

    print(f"Search index built: {len(index)} questions -> {OUTPUT}")

if __name__ == "__main__":
    main()
