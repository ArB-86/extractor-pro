from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass(slots=True)
class Option:
    label: str
    text: str


@dataclass(slots=True)
class Question:

    id: int

    source: str

    chapter: str

    page_start: int

    page_end: int

    question_type: str

    question: str

    options: List[Option] = field(default_factory=list)

    answer: Optional[str] = None

    solution: Optional[str] = None

    difficulty: Optional[str] = None

    topic: Optional[str] = None

    tags: List[str] = field(default_factory=list)

    metadata: dict = field(default_factory=dict)
