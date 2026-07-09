from __future__ import annotations

from pathlib import Path
import csv


class CSVEvaluationReport:

    def save(

        self,

        report,

        path,

    ):

        path = Path(path)

        path.parent.mkdir(

            parents=True,

            exist_ok=True,

        )

        with path.open(

            "w",

            newline="",

            encoding="utf-8",

        ) as f:

            w = csv.writer(f)

            w.writerow(

                [

                    "metric",

                    "value",

                ]

            )

            for section, values in report.items():

                if not isinstance(values, dict):

                    continue

                for k, v in values.items():

                    w.writerow(

                        [

                            f"{section}.{k}",

                            v,

                        ]

                    )
