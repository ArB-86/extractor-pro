from __future__ import annotations

from .gold_dataset import GoldDataset
from .aligner import AlignmentEngine
from .metrics_engine import MetricsEngine
from .error_analyzer import ErrorAnalyzer
from .report_writer import ReportWriter


class EvaluationRunner:

    def __init__(self):

        self.gold = GoldDataset()

        self.aligner = AlignmentEngine()

        self.metrics = MetricsEngine()

        self.errors = ErrorAnalyzer()

        self.writer = ReportWriter()

    def run(

        self,

        predicted,

        gold_path,

        output_dir,

    ):

        gold = self.gold.load(

            gold_path,

        )

        ok, errors = self.gold.validate(

            [

                g.__dict__

                if hasattr(g,"__dict__")

                else {}

                for g in gold

            ]

        )

        if not ok:

            raise RuntimeError(

                "\\n".join(errors)

            )

        alignment = self.aligner.align(

            predicted,

            gold,

        )

        report = self.metrics.compute(

            alignment,

        )

        analysis = self.errors.analyze(

            predicted,

            gold,

            alignment.matched_pairs,

        )

        report["errors"] = {

            "false_positive":

                len(

                    analysis.false_positives

                ),

            "false_negative":

                len(

                    analysis.false_negatives

                ),

            "tags":

                analysis.top_error_tags,

        }

        self.writer.write_all(

            report,

            output_dir,

        )

        return report
