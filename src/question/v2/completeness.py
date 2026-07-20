from __future__ import annotations

import re


class CompletenessScorer:

    QUESTION_WORDS = {
        "what",
        "why",
        "how",
        "which",
        "where",
        "who",
        "when",
        "find",
        "draw",
        "show",
        "prove",
        "calculate",
        "determine",
        "identify",
        "write",
        "state",
        "can",
    }

    @classmethod
    def score(cls, text: str) -> float:

        if not text:
            return 0.0

        score = 0.0

        words = text.lower().split()

        if len(words) > 6:
            score += 0.2

        if any(w in words for w in cls.QUESTION_WORDS):
            score += 0.3

        if "?" in text:
            score += 0.2

        if re.search(r"^\s*(?:q\.?\s*)?\d+", text, re.I):
            score += 0.3

        return min(score, 1.0)
