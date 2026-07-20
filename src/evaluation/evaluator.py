from __future__ import annotations

from src.evaluation.book_metrics import BookMetrics
from src.evaluation.question_matcher import QuestionMatcher


class Evaluator:

    def evaluate(
        self,
        expected: list[str],
        extracted: list[str],
    ) -> BookMetrics:

        metrics = BookMetrics()

        metrics.expected_questions = len(expected)
        metrics.extracted_questions = len(extracted)

        matched = set()

        for exp in expected:

            found = False

            for i, ext in enumerate(extracted):

                if i in matched:
                    continue

                if QuestionMatcher.match(exp, ext):
                    matched.add(i)
                    found = True
                    break

            if found:
                metrics.matched_questions += 1
            else:
                metrics.missed_questions += 1

        metrics.false_positives = (
            metrics.extracted_questions
            - metrics.matched_questions
        )

        return metrics
