from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class QuestionType(str, Enum):
    MCQ = "mcq"
    FILL_IN_BLANK = "fill_in_blank"
    TRUE_FALSE = "true_false"
    SHORT_ANSWER = "short_answer"
    LONG_ANSWER = "long_answer"
    NUMERICAL = "numerical"
    MATCHING = "matching"
    ASSERTION_REASON = "assertion_reason"
    CASE_STUDY = "case_study"
    UNKNOWN = "unknown"


@dataclass(slots=True)
class QuestionContext:
    chapter: str | None = None
    exercise: str | None = None
    section: str | None = None
    topic: str | None = None
    subtopic: str | None = None
    page: int | None = None
    source_type: str = "textbook"  # added


@dataclass(slots=True)
class QuestionCandidate:
    number: str
    text: str = ""
    context: QuestionContext = field(default_factory=QuestionContext)
    qtype: QuestionType = QuestionType.UNKNOWN
    confidence: float = 1.0
    metadata: dict[str, Any] = field(default_factory=dict)
