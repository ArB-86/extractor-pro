from __future__ import annotations

import re

_SPLIT = re.compile(r"(?=(?:^|\s)(\d+)\.\s)")


class QuestionSplitter:

    def split(self, text: str) -> list[str]:

        text = re.sub(r"\s+", " ", text).strip()

        parts = _SPLIT.split(text)

        if len(parts) <= 1:
            return [text]

        questions = []

        i = 1

        while i < len(parts):

            number = parts[i]

            body = parts[i + 1].strip()

            body = re.sub(rf"^{number}\.\s*", "", body)

            questions.append(f"{number}. {body}")

            i += 2

        return questions