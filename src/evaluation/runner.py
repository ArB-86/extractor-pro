from __future__ import annotations

from pathlib import Path

from src.evaluation.benchmark import EvaluationBenchmark
from src.evaluation.json_report import JSONEvaluationReport
from src.evaluation.html_report import HTMLEvaluationReport


class EvaluationRunner:

    def __init__(self):

        self.benchmark = EvaluationBenchmark()

        self.json = JSONEvaluationReport()

        self.html = HTMLEvaluationReport()

    def run(

        self,

        predicted,

        gold,

        output_dir,

    ):

        report = self.benchmark.evaluate(
            predicted,
            gold,
        )

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

        return report
