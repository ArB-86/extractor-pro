from dataclasses import dataclass, field
from typing import Optional

from pipeline.models.question import Question


@dataclass
class ParserState:

    exercise: str = ""

    section: str = ""

    current_question: Optional[Question] = None

    questions: list[Question] = field(default_factory=list)

    question_no: int = 0
