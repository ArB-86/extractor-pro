import json
from pathlib import Path


class ExportPipeline:

    def export_json(
        self,
        dataset,
        output_path,
    ):

        output_path = Path(output_path)

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with open(
            output_path,
            "w",
            encoding="utf-8",
        ) as f:

            json.dump(
                dataset,
                f,
                indent=2,
                ensure_ascii=False,
            )
