from __future__ import annotations

from statistics import mean


class EvaluationStatistics:

    def summary(self, report):

        qm = report["question_metrics"]

        return {

            "precision": qm["precision"],

            "recall": qm["recall"],

            "f1": qm["f1"],

            "exact_match": qm["exact_match_accuracy"],

            "macro_average": round(

                mean(

                    [

                        qm["precision"],

                        qm["recall"],

                        qm["f1"],

                    ]

                ),

                6,

            ),

        }
