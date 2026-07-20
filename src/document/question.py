from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
from typing import Any


@dataclass
class Question:

    question_text: str

    question_id: str = ""

    class_name: str | None = None

    subject: str = "Mathematics"

    chapter: str | None = None

    exercise: str | None = None

    question_number: str | None = None

    question_type: str | None = None

    difficulty: str | None = None

    answer: str | None = None

    solution: str | None = None

    hint: str | None = None

    source_book: str | None = None

    source_page: int | None = None

    source_type: str = "textbook"

    academic_year: str | None = None

    confidence: float = 1.0

    review_required: bool = False

    metadata: dict[str, Any] = field(default_factory=dict)

    sha256: str = ""

    def __post_init__(self):

        # SHA-256 is assigned by the QuestionDeduplicator after
        # normalization and duplicate resolution.
        pass
