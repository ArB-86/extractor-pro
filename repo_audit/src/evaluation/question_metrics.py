from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class QuestionMetrics:
    total_predicted: int = 0
    total_gold: int = 0
    matched: int = 0
    exact_matches: int = 0

    @property
    def precision(self) -> float:
        return 0.0 if self.total_predicted == 0 else self.matched / self.total_predicted

    @property
    def recall(self) -> float:
        return 0.0 if self.total_gold == 0 else self.matched / self.total_gold

    @property
    def f1(self) -> float:
        p = self.precision
        r = self.recall
        return 0.0 if (p + r) == 0 else 2.0 * p * r / (p + r)

    @property
    def exact_match_accuracy(self) -> float:
        return 0.0 if self.total_gold == 0 else self.exact_matches / self.total_gold

    def to_dict(self) -> dict:
        return {
            "total_predicted": self.total_predicted,
            "total_gold": self.total_gold,
            "matched": self.matched,
            "exact_matches": self.exact_matches,
            "precision": round(self.precision, 6),
            "recall": round(self.recall, 6),
            "f1": round(self.f1, 6),
            "exact_match_accuracy": round(self.exact_match_accuracy, 6),
        }
