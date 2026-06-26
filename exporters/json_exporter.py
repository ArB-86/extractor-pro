import json
from dataclasses import asdict


class JSONExporter:

    def export(self, questions, output_file):

        data = []

        for q in questions:
            data.append(asdict(q))

        with open(output_file, "w", encoding="utf8") as f:
            json.dump(
                data,
                f,
                indent=4,
                ensure_ascii=False
            )
