from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Any, List, Optional

from src.dataset.registry import QuestionRegistry
from src.extractor.result import ExtractionResult


class MasterDataset:
    """Central registry for all extracted questions across a document."""

    def __init__(self) -> None:
        self.registry = QuestionRegistry()

    def add(self, questions: List[Any]) -> None:
        """Add a list of Question objects to the dataset."""
        self.registry.extend(questions)

    def all(self) -> List[Any]:
        """Return all questions as a list."""
        return self.registry.all()

    def __len__(self) -> int:
        return len(self.registry)

    def export(
        self,
        output_dir: Path,
        gold_expected: Optional[Path] = None,
    ) -> ExtractionResult:
        """Export the dataset to a JSONL file and return an ExtractionResult."""
        questions = self.registry.all()

        # ---- Export to JSONL ----
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        out_file = output_dir / "master_dataset.jsonl"

        with out_file.open("w", encoding="utf-8") as f:
            for q in questions:
                f.write(json.dumps(asdict(q), ensure_ascii=False) + "\n")

        # ---- Build manifest and statistics ----
        manifest = {
            "total": len(questions),
            "output_file": str(out_file),
        }

        statistics = {
            "total_questions": len(questions),
            "unique_chapters": len({q.chapter for q in questions if q.chapter}),
            "unique_exercises": len({q.exercise for q in questions if q.exercise}),
        }

        # ---- Return ExtractionResult ----
        return ExtractionResult(
            questions=questions,
            manifest=manifest,
            statistics=statistics,
            search_index={},  # placeholder
            output_directory=str(output_dir),
            evaluation=None,
        )
