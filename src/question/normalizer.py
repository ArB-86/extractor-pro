import re

from src.document.question import Question


class QuestionNormalizer:

    def normalize(self, questions: list[Question]) -> list[Question]:

        for q in questions:

            text = q.question_text

            text = re.sub(r"\s+", " ", text)

            text = text.replace(" ,", ",")

            text = text.replace(" .", ".")

            text = text.strip()

            q.question_text = text

        return questions
