from __future__ import annotations

import re


class QuestionSanity:

    START = re.compile(
        r"^\s*(?:Q\.?\s*)?\d+[.)。．﹒․]",
        re.I,
    )

    @classmethod
    def valid(cls, text: str) -> bool:

        if not text:
            return False

        if not cls.START.match(text):
            return False

        if len(text.split()) < 5:
            return False

        if sum(c.isalpha() for c in text) < 15:
            return False

        return True
