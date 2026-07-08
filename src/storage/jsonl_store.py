import json
from pathlib import Path
from dataclasses import asdict


class JSONLStore:

    def write(self, questions, output):

        output = Path(output)

        output.parent.mkdir(parents=True, exist_ok=True)

        with output.open("w", encoding="utf-8") as f:

            for q in questions:
                f.write(json.dumps(asdict(q), ensure_ascii=False) + "\n")
