from pathlib import Path
import json

from src.benchmark.metrics import BenchmarkMetrics


class BenchmarkReport:

    def save(
        self,
        metrics: BenchmarkMetrics,
        output_file,
    ):

        output = Path(output_file)

        output.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        report = {
            "precision": round(metrics.precision, 6),
            "recall": round(metrics.recall, 6),
            "f1": round(metrics.f1, 6),
            "true_positive": metrics.true_positive,
            "false_positive": metrics.false_positive,
            "false_negative": metrics.false_negative,
        }

        with open(output, "w", encoding="utf-8") as f:
            json.dump(
                report,
                f,
                indent=2,
                ensure_ascii=False,
            )
