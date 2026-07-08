from src.document.question import Question

from src.benchmark.metrics import BenchmarkMetrics


class AlignmentEngine:

    @staticmethod
    def _normalize(text: str) -> str:

        return " ".join(
            text.lower().split()
        )

    def evaluate(
        self,
        predicted: list[Question],
        gold: list[Question],
    ) -> BenchmarkMetrics:

        metrics = BenchmarkMetrics()

        pred = {
            self._normalize(q.question_text)
            for q in predicted
        }

        gt = {
            self._normalize(q.question_text)
            for q in gold
        }

        metrics.true_positive = len(
            pred & gt
        )

        metrics.false_positive = len(
            pred - gt
        )

        metrics.false_negative = len(
            gt - pred
        )

        return metrics
