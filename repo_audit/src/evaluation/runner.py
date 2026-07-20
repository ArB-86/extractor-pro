
from __future__ import annotations

from src.evaluation.gold_loader import GoldDatasetLoader
from src.evaluation.aligner import AlignmentEngine
from src.evaluation.json_report import JSONEvaluationReport


class EvaluationRunner:

    def __init__(self):

        self.gold = GoldDatasetLoader()
        self.aligner = AlignmentEngine()
        self.report = JSONEvaluationReport()

    def run(
        self,
        predicted,
        gold_path,
        output_path=None,
        baseline=None,
    ):

        gold = self.gold.load(gold_path)

        alignment = self.aligner.align(
            predicted,
            gold,
        )

        result = {
            "question": alignment.question_metrics.to_dict(),
            "boundary": alignment.boundary_metrics.to_dict(),
            "matched_pairs": len(alignment.matched_pairs),
            "exact_question_matches": alignment.exact_question_matches,
        }

        if output_path:
            self.report.save(
                result,
                output_path,
            )

        return result
