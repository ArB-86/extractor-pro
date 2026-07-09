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

            text = " ".join(q.text.split())

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

            q.text = text

            valid.append(q)

        return valid
