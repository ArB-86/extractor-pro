from dataclasses import dataclass, field


@dataclass(slots=True)
class Question:

    id: int

    source: str

    chapter: str

    exercise: str

    page_start: int

    page_end: int

    question_type: str

    question: str

    options: dict = field(default_factory=dict)

    answer: str | None = None

    solution: str | None = None