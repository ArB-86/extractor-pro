from __future__ import annotations

import re

from rapidfuzz import fuzz


class QuestionMatcher:

    SIMILARITY = 98.0

    @staticmethod
    def normalize(text: str) -> str:
        text = text.lower()
        text = re.sub(r"q\.?\s*\d+[.)]?", "", text)
        text = re.sub(r"[^\w\s]", " ", text)
        text = re.sub(r"\s+", " ", text)
        return text.strip()

    @classmethod
    def match(cls, expected: str, extracted: str) -> bool:
        return (
            fuzz.token_sort_ratio(
                cls.normalize(expected),
                cls.normalize(extracted),
            )
            >= cls.SIMILARITY
        )
