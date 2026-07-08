from __future__ import annotations

from dataclasses import asdict
from hashlib import sha256
from pathlib import Path
import json
from typing import Iterable

from src.document.question import Question


class DatasetBuilder:
    """
    Builds the canonical master dataset.

    Responsibilities
    ----------------
    - Normalize questions
    - Remove duplicates
    - Assign stable IDs
    - Attach metadata
    - Export dataset
    """

    def __init__(self):
        self.questions: list[Question] = []

    def add(self, question: Question) -> None:
        self.questions.append(question)

    def extend(self, questions: Iterable[Question]) -> None:
        self.questions.extend(questions)

    def _fingerprint(self, q: Question) -> str:
        text = " ".join(q.question_text.lower().split())
        return sha256(text.encode()).hexdigest()

    def deduplicate(self) -> None:
        seen = {}
        unique = []

        for q in self.questions:
            fp = self._fingerprint(q)

            if fp in seen:
                continue

            seen[fp] = True
            unique.append(q)

        self.questions = unique

    def assign_ids(self) -> None:
        for i, q in enumerate(self.questions, start=1):

            if getattr(q, "question_id", None):
                continue

            q.question_id = f"QF-{i:08d}"

    def build(self) -> dict:

        self.deduplicate()

        self.assign_ids()

        return {
            "total_questions": len(self.questions),
            "questions": [asdict(q) for q in self.questions],
        }

    def export_json(self, output: str | Path):

        output = Path(output)

        output.parent.mkdir(parents=True, exist_ok=True)

        with open(output, "w", encoding="utf-8") as f:

            json.dump(
                self.build(),
                f,
                indent=2,
                ensure_ascii=False,
            )
