from __future__ import annotations

from collections import defaultdict


class ConfusionMatrix:

    def build(self, gold, predicted):

        matrix = defaultdict(lambda: defaultdict(int))

        matched = min(len(gold), len(predicted))

        for i in range(matched):

            g = getattr(
                gold[i],
                "question_type",
                "unknown",
            )

            p = getattr(
                predicted[i],
                "question_type",
                "unknown",
            )

            matrix[g][p] += 1

        return {
            k: dict(v)
            for k, v in matrix.items()
        }
