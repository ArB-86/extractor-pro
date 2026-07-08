from src.document.question import Question


class QuestionClassifier:

    def classify(self, questions: list[Question]) -> list[Question]:

        for q in questions:

            text = q.question_text.lower()

            if "prove" in text:
                q.question_type = "proof"

            elif "find" in text:
                q.question_type = "numerical"

            elif "verify" in text:
                q.question_type = "verification"

            elif "construct" in text:
                q.question_type = "construction"

            else:
                q.question_type = "general"

        return questions
