import json
from pathlib import Path


class CurriculumReport:

    def save(self, audit, output):

        output = Path(output)

        output.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with open(
            output,
            "w",
            encoding="utf-8",
        ) as f:

            json.dump(
                audit,
                f,
                indent=2,
                ensure_ascii=False,
            )
