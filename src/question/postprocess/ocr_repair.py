from __future__ import annotations

import re

from src.document.question import Question


class OCRRepair:

    REPLACEMENTS = (
        (r"\bCount t the\b", "Count the"),
        (r"\bnumber r of\b", "number of"),
        (r"\bHow little there\b", "How many little"),
        (r"\bg give\b", "give"),
        (r"\bCan think of\b", "Can you think of"),
        (r"\bWhya\b", "Why"),
        (r"\bcalleds\b", "called"),
        (r"\bseguences\b", "sequences"),
        (r"\bteum\b", "term"),
        (r"\bnok\b", ""),
    )

    def process(
        self,
        questions: list[Question],
    ) -> list[Question]:

        for q in questions:

            text = q.question_text

            for pattern, repl in self.REPLACEMENTS:
                text = re.sub(
                    pattern,
                    repl,
                    text,
                    flags=re.IGNORECASE,
                )

            text = re.sub(r"\s+", " ", text).strip()

            q.question_text = text

        return questions
