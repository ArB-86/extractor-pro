from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict


@dataclass(slots=True)
class EvaluationMetrics:
    true_positive: int = 0
    false_positive: int = 0
    false_negative: int = 0

    @property
    def precision(self) -> float:
        denom = self.true_positive + self.false_positive
        return 0.0 if denom == 0 else self.true_positive / denom

    @property
    def recall(self) -> float:
        denom = self.true_positive + self.false_negative
        return 0.0 if denom == 0 else self.true_positive / denom

    @property
    def f1(self) -> float:
        p = self.precision
        r = self.recall
        return 0.0 if (p + r) == 0 else 2.0 * p * r / (p + r)

    @property
    def accuracy(self) -> float:
        denom = self.true_positive + self.false_positive + self.false_negative
        return 0.0 if denom == 0 else self.true_positive / denom

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data.update(
            {
                "precision": round(self.precision, 6),
                "recall": round(self.recall, 6),
                "f1": round(self.f1, 6),
                "accuracy": round(self.accuracy, 6),
            }
        )
        return data
