from src.document.question import Question


class QuestionEnricher:

    def enrich(
        self,
        questions: list[Question],
    ) -> list[Question]:

        for q in questions:

            if not q.difficulty:

                words = len(q.question_text.split())

                if words <= 15:
                    q.difficulty = "easy"

                elif words <= 40:
                    q.difficulty = "medium"

                else:
                    q.difficulty = "hard"

            if not q.metadata:

                q.metadata = {}

            q.metadata["has_answer"] = q.answer is not None

            q.metadata["has_solution"] = (
                q.solution is not None
            )

            q.metadata["word_count"] = len(
                q.question_text.split()
            )

            q.metadata["character_count"] = len(
                q.question_text
            )

        return questions
