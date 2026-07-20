from __future__ import annotations

import re
from hashlib import sha256

from rapidfuzz import fuzz

from src.document.question import Question


class QuestionDeduplicator:

    SIMILARITY = 98.0

    @staticmethod
    def _normalize(text: str) -> str:

        text = text.lower()

        text = text.replace("ﬁ", "fi")
        text = text.replace("ﬂ", "fl")

        text = re.sub(r"\s+", " ", text)

        text = re.sub(r"[^\w ]", "", text)

        return text.strip()

    def deduplicate(
        self,
        questions: list[Question],
    ) -> list[Question]:

        unique: list[Question] = []

        groups: dict[
            tuple[str | None, str | None, str | None],
            list[Question],
        ] = {}

        for q in questions:

            key = (
                q.chapter,
                q.exercise,
                q.question_number,
            )

            norm = self._normalize(
                q.question_text,
            )

            duplicate = False

            for existing in groups.get(key, ()):

                score = fuzz.ratio(
                    norm,
                    self._normalize(
                        existing.question_text,
                    ),
                )

                if score >= self.SIMILARITY:

                    duplicate = True

                    if q.confidence > existing.confidence:

                        existing.question_text = q.question_text
                        existing.confidence = q.confidence
                        existing.metadata = q.metadata

                    break

            if duplicate:
                continue

            digest = sha256(
                (
                    f"{q.chapter}|"
                    f"{q.exercise}|"
                    f"{q.question_number}|"
                    f"{norm}"
                ).encode("utf-8")
            ).hexdigest()

            q.sha256 = digest

            groups.setdefault(
                key,
                [],
            ).append(q)

            unique.append(q)

        return unique
