from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class BoundaryMetrics:
    exact_match: int = 0
    boundary_match: int = 0
    total: int = 0

    @property
    def exact_match_accuracy(self) -> float:
        return 0.0 if self.total == 0 else self.exact_match / self.total

    @property
    def boundary_accuracy(self) -> float:
        return 0.0 if self.total == 0 else self.boundary_match / self.total

    def to_dict(self) -> dict:
        return {
            "exact_match": self.exact_match,
            "boundary_match": self.boundary_match,
            "total": self.total,
            "exact_match_accuracy": round(self.exact_match_accuracy, 6),
            "boundary_accuracy": round(self.boundary_accuracy, 6),
        }
