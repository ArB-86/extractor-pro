from src.document.question import Question


class QuestionValidator:

    MIN_LENGTH = 10

    def validate(self, question: Question) -> bool:

        if not question.question_text:
            return False

        if len(question.question_text.strip()) < self.MIN_LENGTH:
            return False

        if not question.chapter:
            return False

        return True

    def validate_many(self, questions: list[Question]) -> list[Question]:

        return [
            q
            for q in questions
            if self.validate(q)
        ]
