from __future__ import annotations

import json
from pathlib import Path

ROOT = Path("datasets")
OUT = ROOT / "merged"

OUT.mkdir(parents=True, exist_ok=True)

output_file = OUT / "master_questions.jsonl"

books = 0
questions = 0
skipped = 0

with output_file.open("w", encoding="utf-8") as out:

    for file in sorted(ROOT.rglob("master_dataset.jsonl")):

        books += 1

        book = file.parent.name

        with file.open("r", encoding="utf-8") as f:

            for line in f:

                line = line.strip()

                if not line:
                    continue

                try:

                    obj = json.loads(line)

                except Exception:

                    skipped += 1
                    continue

                obj["book_id"] = book

                out.write(
                    json.dumps(
                        obj,
                        ensure_ascii=False,
                    )
                    + "\n"
                )

                questions += 1

print("=" * 60)
print("Merge Complete")
print("=" * 60)
print("Books      :", books)
print("Questions  :", questions)
print("Skipped    :", skipped)
print("Output     :", output_file)
print("=" * 60)
