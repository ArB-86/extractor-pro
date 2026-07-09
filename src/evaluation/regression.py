from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json
from typing import Any


@dataclass(slots=True)
class RegressionResult:
    passed: bool
    current: dict[str, Any]
    baseline: dict[str, Any]
    deltas: dict[str, float]


class RegressionComparator:
    def load_baseline(self, path: str | Path) -> dict[str, Any]:
        path = Path(path)
        if not path.exists():
            return {}
        return json.loads(path.read_text(encoding="utf-8"))

    def compare(self, current: dict[str, Any], baseline: dict[str, Any]) -> RegressionResult:
        deltas: dict[str, float] = {}
        for key in ("precision", "recall", "f1", "exact_match_accuracy", "boundary_accuracy"):
            cur = float(current.get(key, 0.0))
            base = float(baseline.get(key, 0.0))
            deltas[key] = round(cur - base, 6)

        passed = all(delta >= 0 for delta in deltas.values())
        return RegressionResult(
            passed=passed,
            current=current,
            baseline=baseline,
            deltas=deltas,
        )

    def compare_and_report(
        self,
        current: dict[str, Any],
        baseline_path: str | Path,
    ) -> RegressionResult:
        baseline = self.load_baseline(baseline_path)
        return self.compare(current, baseline)
