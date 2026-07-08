from src.question.models import QuestionCandidate


class QuestionMerger:

    MIN_LENGTH = 25

    def merge(
        self,
        questions: list[QuestionCandidate],
    ) -> list[QuestionCandidate]:

        if not questions:
            return []

        merged = []

        current = questions[0]

        for nxt in questions[1:]:

            if (
                len(current.text) < self.MIN_LENGTH
                and current.context.chapter == nxt.context.chapter
                and current.context.exercise == nxt.context.exercise
            ):

                current.text += "\n" + nxt.text

                continue

            merged.append(current)

            current = nxt

        merged.append(current)

        return merged
