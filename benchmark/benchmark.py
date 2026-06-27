
from __future__ import annotations

from collections import Counter


class Benchmark:

    def evaluate(self, predictions, golden):

        total = len(golden)

        if total == 0:
            return {}

        correct = 0

        field_scores = Counter()

        for pred, gt in zip(predictions, golden):

            if pred["question"] == gt["question"]:
                field_scores["question"] += 1

            if pred["question_type"] == gt["question_type"]:
                field_scores["question_type"] += 1

            if pred["difficulty"] == gt["difficulty"]:
                field_scores["difficulty"] += 1

            if pred["topic"] == gt["topic"]:
                field_scores["topic"] += 1

            if pred == gt:
                correct += 1

        return {

            "samples": total,

            "exact_match": round(
                correct / total * 100,
                2
            ),

            "question_accuracy": round(
                field_scores["question"] / total * 100,
                2
            ),

            "question_type_accuracy": round(
                field_scores["question_type"] / total * 100,
                2
            ),

            "difficulty_accuracy": round(
                field_scores["difficulty"] / total * 100,
                2
            ),

            "topic_accuracy": round(
                field_scores["topic"] / total * 100,
                2
            ),
        }
