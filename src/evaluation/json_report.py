from __future__ import annotations

from pathlib import Path
import json
from typing import Any


class JSONEvaluationReport:
    def save(self, report: dict[str, Any], output_path: str | Path) -> Path:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(
            json.dumps(report, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        return output_path
