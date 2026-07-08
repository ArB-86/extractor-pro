import re

from src.document.question import Question


class QuestionParser:

    QUESTION_PATTERN = re.compile(
        r"^\s*(\d+)[\.\)]\s+",
        re.MULTILINE,
    )

    def parse(self, questions: list[Question]) -> list[Question]:

        for q in questions:

            m = self.QUESTION_PATTERN.match(q.question_text)

            if m:
                q.question_number = m.group(1)

        return questions
