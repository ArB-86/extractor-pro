from __future__ import annotations

from pathlib import Path
from typing import Any

from src.document.question import Question
from src.evaluation.benchmark import EvaluationBenchmark


class EvaluationRunner:
    def __init__(self, similarity_threshold: float = 0.92):
        self.benchmark = EvaluationBenchmark(similarity_threshold=similarity_threshold)

    def run(
        self,
        predicted_questions: list[Question],
        gold_path: str | Path,
        output_path: str | Path | None = None,
    ) -> dict[str, Any]:
        gold = self.benchmark.load_gold(gold_path)
        report = self.benchmark.evaluate(predicted_questions, gold)
        if output_path is not None:
            self.benchmark.save_report(report, output_path)
        return report
