from dataclasses import dataclass


@dataclass
class Question:

    question_id: str

    question_text: str

    answer: str | None

    chapter: str | None

    difficulty: str | None
