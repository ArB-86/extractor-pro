from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable
import json
import csv


@dataclass(slots=True)
class GoldSample:
    question_id: str
    question_text: str
    chapter: str | None = None
    exercise: str | None = None
    question_number: str | None = None
    question_type: str | None = None
    source_book: str | None = None
    source_page: int | None = None
    metadata: dict[str, Any] | None = None


class GoldDatasetLoader:
    def load(self, path: str | Path) -> list[GoldSample]:
        path = Path(path)
        if path.suffix.lower() in {".json", ".jsonl"}:
            return self._load_json_or_jsonl(path)
        if path.suffix.lower() == ".csv":
            return self._load_csv(path)
        raise ValueError(f"Unsupported gold dataset format: {path.suffix}")

    def _load_json_or_jsonl(self, path: Path) -> list[GoldSample]:
        text = path.read_text(encoding="utf-8").strip()
        if not text:
            return []
        if text.startswith("["):
            rows = json.loads(text)
        else:
            rows = [json.loads(line) for line in text.splitlines() if line.strip()]
        return [self._row_to_sample(row) for row in rows]

    def _load_csv(self, path: Path) -> list[GoldSample]:
        with path.open("r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            return [self._row_to_sample(row) for row in reader]

    def _row_to_sample(self, row: dict[str, Any]) -> GoldSample:
        return GoldSample(
            question_id=str(row.get("question_id", "")).strip(),
            question_text=str(row.get("question_text") or row.get("text") or "").strip(),
            chapter=(row.get("chapter") or None),
            exercise=(row.get("exercise") or None),
            question_number=(row.get("question_number") or None),
            question_type=(row.get("question_type") or None),
            source_book=(row.get("source_book") or None),
            source_page=self._to_int(row.get("source_page")),
            metadata=row.get("metadata") if isinstance(row.get("metadata"), dict) else None,
        )

    def _to_int(self, value: Any) -> int | None:
        if value is None or value == "":
            return None
        try:
            return int(value)
        except Exception:
            return None
