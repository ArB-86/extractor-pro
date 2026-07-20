from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class ChapterMetrics:
    total_predicted: int = 0
    total_gold: int = 0
    matched: int = 0

    @property
    def accuracy(self) -> float:
        return 0.0 if self.total_gold == 0 else self.matched / self.total_gold

    def to_dict(self) -> dict:
        return {
            "total_predicted": self.total_predicted,
            "total_gold": self.total_gold,
            "matched": self.matched,
            "accuracy": round(self.accuracy, 6),
        }
