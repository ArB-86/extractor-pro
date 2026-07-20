from dataclasses import dataclass, field
from typing import Any

@dataclass
class Question:

    question_id: str = ""

    source: str = ""

    board: str = "CBSE"

    publisher: str = "NCERT"

    edition: str = "2026"

    language: str = "English"

    class_no: int = 0

    subject: str = "Mathematics"

    chapter_no: int = 0

    chapter: str = ""

    section: str = ""

    exercise: str = ""

    question_no: str = ""

    sub_question: str = ""

    page_start: int = 0

    page_end: int = 0

    question_type: str = ""

    difficulty: str = "unknown"

    bloom: str = ""

    topic: str = ""

    subtopic: str = ""

    estimated_time: int = 0

    marks: int = 0

    question: str = ""

    options: dict = field(default_factory=dict)

    answer: str = ""

    solution: str = ""

    hints: list = field(default_factory=list)

    formulae: list = field(default_factory=list)

    figures: list = field(default_factory=list)

    tables: list = field(default_factory=list)

    keywords: list = field(default_factory=list)

    concepts: list = field(default_factory=list)

    prerequisites: list = field(default_factory=list)

    competencies: list = field(default_factory=list)

    learning_outcomes: list = field(default_factory=list)

    bbox: list = field(default_factory=list)

    embedding_id: str = ""

    content_hash: str = ""

    parser_version: str = "3"

    verified: bool = False

    validation_score: float = 0.0

    metadata: dict[str, Any] = field(default_factory=dict)
