from hashlib import sha256

from src.document.question import Question


class QuestionDeduplicator:

    def deduplicate(
        self,
        questions: list[Question],
    ) -> list[Question]:

        seen = set()

        unique = []

        for q in questions:

            key = sha256(
                " ".join(
                    q.question_text.lower().split()
                ).encode("utf-8")
            ).hexdigest()

            if key in seen:
                continue

            seen.add(key)

            q.sha256 = key

            unique.append(q)

        return unique
