import json
from pathlib import Path


class JSONLExporter:

    def export(self, questions, output_path):

        output_path = Path(output_path)

        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:

            for q in questions:
                f.write(json.dumps(q, ensure_ascii=False) + "\n")
