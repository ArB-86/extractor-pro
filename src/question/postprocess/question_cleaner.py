from __future__ import annotations

import re

from src.document.question import Question


class QuestionCleaner:

    PREFIX = re.compile(
        r"^\s*(?:Question\s*)?Q?\.?\s*(\d+)\s*[.)。．﹒]?\s*",
        re.IGNORECASE,
    )

    def process(
        self,
        questions: list[Question],
    ) -> list[Question]:

        for q in questions:

            text = q.question_text.strip()

            m = self.PREFIX.match(text)

            if m:

                if not q.question_number:
                    q.question_number = m.group(1)

                text = text[m.end():].strip()

            text = re.sub(r"\s+", " ", text)

            text = text.replace(" ?", "?")
            text = text.replace(" .", ".")
            text = text.replace(" ,", ",")

            q.question_text = text

        return questions
