from __future__ import annotations

import re

from models.question import Question


# Matches:
# 1.
# 7. Question text
# 12.
QUESTION_START = re.compile(r"^\s*([1-9][0-9]*)\.(?:\s|\n|$)")


class QuestionParser:

    def __init__(self, section):

        self.section = section

    def parse(self):

        questions = []

        current = None

        for block in self.section.blocks:

            text = block.text.strip()

            if not text:
                continue

            m = QUESTION_START.match(text)

            if m:

                if current is not None:
                    questions.append(current)

                current = Question(
                    id=int(m.group(1)),
                    source="NCERT Exemplar",
                    chapter="",
                    exercise=self.section.title,
                    page_start=block.page,
                    page_end=block.page,
                    question_type="unknown",
                    question=text,
                )

                continue

            if current is not None:

                current.question += "\n" + text
                current.page_end = block.page

        if current is not None:
            questions.append(current)

        return questions