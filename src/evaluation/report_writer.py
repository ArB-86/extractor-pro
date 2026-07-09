from __future__ import annotations

from pathlib import Path
from typing import Any

from .json_report import JSONEvaluationReport
from .html_report import HTMLEvaluationReport
from .csv_report import CSVEvaluationReport


class ReportWriter:

    def __init__(self):

        self.json = JSONEvaluationReport()

        self.html = HTMLEvaluationReport()

        self.csv = CSVEvaluationReport()

    def write_all(

        self,

        report: dict[str, Any],

        output_dir: str | Path,

    ) -> None:

        output_dir = Path(output_dir)

        output_dir.mkdir(

            parents=True,

            exist_ok=True,

        )

        self.json.save(

            report,

            output_dir / "evaluation.json",

        )

        self.html.save(

            report,

            output_dir / "evaluation.html",

        )

        self.csv.save(

            report,

            output_dir / "evaluation.csv",

        )
