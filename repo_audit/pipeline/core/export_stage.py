
from pipeline.core.stage import Stage

import json
from dataclasses import asdict


class ExportStage(Stage):

    def __init__(self, output_file):

        self.output_file = output_file

    def run(self, context):

        data = [

            asdict(q)

            for q in context.questions

        ]

        with open(
            self.output_file,
            "w",
            encoding="utf8"
        ) as f:

            json.dump(
                data,
                f,
                indent=4,
                ensure_ascii=False
            )

        return context
