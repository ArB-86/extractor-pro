from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
from typing import Any

from src.document.question import Question
from src.evaluation.aligner import AlignmentEngine
from src.evaluation.error_analyzer import ErrorAnalyzer
from src.evaluation.gold_loader import GoldDatasetLoader
from src.evaluation.json_report import JSONEvaluationReport


class EvaluationBenchmark:
    def __init__(self, similarity_threshold: float = 0.92):
        self.loader = GoldDatasetLoader()
        self.aligner = AlignmentEngine(similarity_threshold=similarity_threshold)
        self.errors = ErrorAnalyzer()
        self.report = JSONEvaluationReport()

    def load_gold(self, path: str | Path):
        return self.loader.load(path)

    def evaluate(self, predicted: list[Question], gold: list[object]) -> dict[str, Any]:
        alignment = self.aligner.align(predicted, gold)
        error_summary = self.errors.analyze(predicted, gold, alignment.matched_pairs)

        payload = {
            "question_metrics": alignment.question_metrics.to_dict(),
            "boundary_metrics": alignment.boundary_metrics.to_dict(),
            "error_summary": {
                "false_positive_count": len(error_summary.false_positives),
                "false_negative_count": len(error_summary.false_negatives),
                "top_error_tags": error_summary.top_error_tags,
            },
            "matched_pairs": [
                {
                    "predicted": asdict(p),
                    "gold": g.__dict__ if hasattr(g, "__dict__") else dict(g),
                }
                for p, g in alignment.matched_pairs
            ],
        }
        return payload

    def save_report(self, report: dict[str, Any], output_path: str | Path) -> Path:
        return self.report.save(report, output_path)
