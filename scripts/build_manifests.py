from __future__ import annotations

import json
from pathlib import Path

ROOT = Path("datasets")


def main():

    for dataset in ROOT.rglob("master_dataset.jsonl"):

        rows = []

        with dataset.open(
            "r",
            encoding="utf-8",
        ) as f:

            for line in f:

                if line.strip():

                    rows.append(
                        json.loads(line)
                    )

        manifest = {

            "book": dataset.parent.name,

            "questions": len(rows),

            "chapters": sorted(
                {
                    x.get("chapter")
                    for x in rows
                    if x.get("chapter")
                }
            ),

        }

        with (
            dataset.parent
            / "manifest.json"
        ).open(
            "w",
            encoding="utf-8",
        ) as f:

            json.dump(
                manifest,
                f,
                indent=2,
                ensure_ascii=False,
            )

        print(dataset.parent)


if __name__ == "__main__":

    main()
