from __future__ import annotations

import re


class OCRLanguageRepair:
    """
    Repairs common OCR language corruption using token context.
    """

    REPAIRS = [
        (r"\bCan you\s+[a-z]\s+give\b", "Can you give"),
        (r"\bCan explain why you\b", "Can you explain why"),
        (r"\bCount\s+[a-z]\s+the\b", "Count the"),
        (r"\bnumber\s+[a-z]\s+of\b", "number of"),
        (r"\bWhat about\s+the\s+number\s+of\b", "What about the number of"),
        (r"\bHow\s+little\s+triangles\s+there\b", "How many little triangles are there"),
        (r"\bHow\s+little\s+there\b", "How many little"),
        (r"\bWhich sequence doyou\b", "Which sequence do you"),
        (r"\bdoyoug\b", "do you get"),
        (r"\bThatis\b", "That is"),
    ]

    @classmethod
    def repair(cls, text: str) -> str:

        if not text:
            return ""

        for pattern, replacement in cls.REPAIRS:
            text = re.sub(
                pattern,
                replacement,
                text,
                flags=re.I,
            )

        return text
