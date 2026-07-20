from __future__ import annotations

import json
from pathlib import Path

ROOT = Path("datasets")


def main():

    for dataset in ROOT.rglob("master_dataset.jsonl"):

        rows = []

        with dataset.open(
            encoding="utf-8",
        ) as f:

            rows = [
                json.loads(x)
                for x in f
                if x.strip()
            ]

        stats = {

            "questions": len(rows),

            "chapters": len(
                {
                    x.get("chapter")
                    for x in rows
                    if x.get("chapter")
                }
            ),

            "pages": len(
                {
                    x.get("page")
                    for x in rows
                    if x.get("page") is not None
                }
            ),

        }

        with (
            dataset.parent
            / "statistics.json"
        ).open(
            "w",
            encoding="utf-8",
        ) as f:

            json.dump(
                stats,
                f,
                indent=2,
            )


if __name__ == "__main__":

    main()
