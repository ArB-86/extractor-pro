from __future__ import annotations

import hashlib
import json
from pathlib import Path

INPUT = Path("cache_output/gegp101/master_dataset.jsonl")
OUTPUT = Path("datasets/gold/class6/mathematics/gegp101_gold.jsonl")


def stable_id(chapter, exercise, number, text):
    key = "|".join(
        [
            chapter or "",
            exercise or "",
            number or "",
            text.strip(),
        ]
    )
    return hashlib.sha256(
        key.encode("utf-8")
    ).hexdigest()[:16]


def main():

    if not INPUT.exists():
        raise FileNotFoundError(INPUT)

    OUTPUT.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    written = 0

    with INPUT.open(
        encoding="utf-8",
    ) as fin, OUTPUT.open(
        "w",
        encoding="utf-8",
    ) as fout:

        for line in fin:

            if not line.strip():
                continue

            q = json.loads(line)

            question_text = (
                q.get("question_text")
                or ""
            ).strip()

            if not question_text:
                continue

            record = {

                "question_id": stable_id(
                    q.get("chapter"),
                    q.get("exercise"),
                    q.get("question_number"),
                    question_text,
                ),

                "question_text": question_text,

                "chapter": q.get("chapter"),

                "exercise": q.get("exercise"),

                "question_number": q.get("question_number"),

                "question_type": q.get("question_type"),

                "source_book": q.get("source_book"),

                "source_page": q.get("source_page"),

                "answer": q.get("answer"),

                "solution": q.get("solution"),

                "verified": False,

                "review_status": "pending",

                "review_notes": "",

                "metadata": q.get(
                    "metadata",
                    {},
                ),
            }

            fout.write(
                json.dumps(
                    record,
                    ensure_ascii=False,
                )
                + "\n"
            )

            written += 1

    print("=" * 70)
    print("Gold dataset created")
    print("Questions :", written)
    print("Output    :", OUTPUT)
    print("=" * 70)


if __name__ == "__main__":
    main()
