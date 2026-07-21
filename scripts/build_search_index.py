from __future__ import annotations

import json
import pickle
from pathlib import Path

INPUT = Path("datasets/merged/master_questions.jsonl")
OUTPUT = Path("datasets/search_index.pkl")


def main() -> None:
    if not INPUT.exists():
        raise FileNotFoundError(INPUT)

    index = []
    with INPUT.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            q = json.loads(line)
            index.append(
                {
                    "question_text": q.get("question_text", ""),
                    "chapter": q.get("chapter"),
                    "question_number": q.get("question_number"),
                    "source_page": q.get("source_page"),
                    "answer": q.get("answer"),
                }
            )

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("wb") as f:
        pickle.dump(index, f)

    print(f"Search index built: {len(index)} questions -> {OUTPUT}")


if __name__ == "__main__":
    main()
