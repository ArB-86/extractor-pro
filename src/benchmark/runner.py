from src.benchmark.evaluator import BenchmarkEvaluator
from src.benchmark.report import BenchmarkReport


class BenchmarkRunner:

    def __init__(self):

        self.evaluator = BenchmarkEvaluator()

        self.report = BenchmarkReport()

    def run(
        self,
        predicted,
        gold,
        output,
    ):

        metrics = self.evaluator.evaluate(
            predicted,
            gold,
        )

        self.report.save(
            metrics,
            output,
        )

        return metrics
