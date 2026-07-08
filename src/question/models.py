from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class QuestionType(str, Enum):

    UNKNOWN = "unknown"
    MCQ = "mcq"
    SHORT = "short"
    LONG = "long"
    FILL = "fill"
    TRUE_FALSE = "true_false"
    ASSERTION_REASON = "assertion_reason"
    CASE_STUDY = "case_study"
    PROOF = "proof"
    CONSTRUCTION = "construction"
    HOTS = "hots"
    ACTIVITY = "activity"


@dataclass(slots=True)
class QuestionContext:

    chapter: str | None = None

    exercise: str | None = None

    topic: str | None = None

    subtopic: str | None = None

    page: int | None = None


@dataclass(slots=True)
class QuestionCandidate:

    number: str

    text: str

    qtype: QuestionType = QuestionType.UNKNOWN

    context: QuestionContext = field(
        default_factory=QuestionContext
    )

    confidence: float = 1.0

    metadata: dict = field(
        default_factory=dict
    )
