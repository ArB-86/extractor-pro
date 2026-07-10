from src.document.question import Question


class QuestionRegistry:

    def __init__(self):

        self._questions = {}

    def add(self, question: Question):

        print(
            "[Registry]",
            type(question).__name__,
            "sha256=",
            getattr(question, "sha256", None),
        )

        self._questions[getattr(question, "sha256", None)] = question

        print("[Registry] size =", len(self._questions))

    def extend(self, questions):

        for q in questions:
            self.add(q)

    def all(self):

        return list(self._questions.values())

    def __len__(self):

        return len(self._questions)
