import re

from src.document.question import Question


class QuestionFilter:

    MIN_LENGTH = 15

    NOISE = (
        "summary",
        "historical note",
        "contents",
        "index",
        "acknowledgement",
    )

    EQUATION_ONLY = re.compile(
        r"^[\d\s+\-*/=().,^]+$"
    )

    def keep(self, question: Question) -> bool:

        text = question.question_text.strip()

        if len(text) < self.MIN_LENGTH:
            return False

        lower = text.lower()

        if any(n in lower for n in self.NOISE):
            return False

        if self.EQUATION_ONLY.fullmatch(text):
            return False

        return True

    def apply(
        self,
        questions: list[Question],
    ) -> list[Question]:

        return [
            q
            for q in questions
            if self.keep(q)
        ]
