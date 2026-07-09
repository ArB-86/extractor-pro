from __future__ import annotations

import re

from src.question.models import QuestionCandidate


class QuestionValidator:

    MIN_WORDS = 3

    MAX_WORDS = 1200

    INVALID_START = (
        "chapter",
        "exercise",
        "summary",
        "contents",
        "index",
    )

    PAGE_ONLY = re.compile(r"^\d+$")

    def validate(
        self,
        questions: list[QuestionCandidate],
    ) -> list[QuestionCandidate]:

        valid = []

        for q in questions:

            text = re.sub(
                r"\s+",
                " ",
                q.text,
            ).strip()

            text = re.sub(
                r"(\b\d+[.)])\s+\1",
                r"\1",
                text,
            )

            if not text:
                continue

            if self.PAGE_ONLY.fullmatch(text):
                continue

            if len(text.split()) < self.MIN_WORDS:
                continue

            if len(text.split()) > self.MAX_WORDS:
                continue

            if text.lower().startswith(self.INVALID_START):
                continue

            alpha = sum(c.isalpha() for c in text)

            if alpha < 3:
                continue

            if re.fullmatch(r"[\W\d_ ]+", text):
                continue

            if len(text) < 12:
                continue

            q.text = text

            valid.append(q)

        return valid
