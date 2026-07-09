
from __future__ import annotations

import json
from pathlib import Path


class RegressionTracker:

    def compare(self, current: dict, baseline_path: str | None):

        if not baseline_path:
            return {}

        path = Path(baseline_path)

        if not path.exists():
            return {}

        baseline = json.loads(path.read_text())

        diff = {}

        for section, metrics in current.items():

            if not isinstance(metrics, dict):
                continue

            previous = baseline.get(section, {})

            diff[section] = {}

            for key, value in metrics.items():

                if isinstance(value, (int, float)):

                    diff[section][key] = value - previous.get(key, 0)

        return diff
