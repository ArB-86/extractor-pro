from __future__ import annotations

from src.evaluation.book_metrics import BookMetrics


class EvaluationReport:

    @staticmethod
    def print(metrics: BookMetrics) -> None:

        print("=" * 60)
        print("EXTRACTION EVALUATION")
        print("=" * 60)

        print(f"Expected Questions : {metrics.expected_questions}")
        print(f"Extracted Questions: {metrics.extracted_questions}")
        print(f"Matched Questions  : {metrics.matched_questions}")
        print(f"Missed Questions   : {metrics.missed_questions}")
        print(f"False Positives    : {metrics.false_positives}")

        print(f"Precision          : {metrics.precision:.2%}")
        print(f"Recall             : {metrics.recall:.2%}")
        print(f"F1 Score           : {metrics.f1:.2%}")

        print("=" * 60)
