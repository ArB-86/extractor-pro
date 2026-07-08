from src.document.question import Question


class QuestionRegistry:

    def __init__(self):

        self._questions = {}

    def add(self, question: Question):

        self._questions[question.sha256] = question

    def extend(self, questions):

        for q in questions:
            self.add(q)

    def all(self):

        return list(self._questions.values())

    def __len__(self):

        return len(self._questions)
