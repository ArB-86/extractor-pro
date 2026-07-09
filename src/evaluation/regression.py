from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json


@dataclass(slots=True)
class RegressionResult:

    passed: bool

    deltas: dict


class RegressionComparator:

    IMPORTANT = (
        "precision",
        "recall",
        "f1",
        "accuracy",
    )

    def compare(
        self,
        baseline: dict,
        current: dict,
    ) -> RegressionResult:

        delta = {}

        passed = True

        for key in self.IMPORTANT:

            b = float(
                baseline.get(key, 0)
            )

            c = float(
                current.get(key, 0)
            )

            delta[key] = round(
                c - b,
                6,
            )

            if c < b:

                passed = False

        return RegressionResult(
            passed=passed,
            deltas=delta,
        )

    def save(
        self,
        result: RegressionResult,
        path: str | Path,
    ):

        Path(path).write_text(

            json.dumps(
                {
                    "passed": result.passed,
                    "deltas": result.deltas,
                },
                indent=2,
            ),
            encoding="utf-8",
        )
