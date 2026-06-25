from __future__ import annotations

import re

from models.question import Question


QUESTION_NUMBER = re.compile(r"^\s*\d+\.")   # matches "1." and "1. Graphically..."


class QuestionParser:

    def __init__(self, section):

        self.section = section

    def parse(self):

        questions = []

        current = None

        qid = 1

        for block in self.section.blocks:

            text = block.text.strip()

            if not text:
                continue

            if QUESTION_NUMBER.match(text):

                if current:

                    questions.append(current)

                current = Question(
                    id=qid,
                    source="NCERT Exemplar",
                    chapter="",
                    page_start=block.page,
                    page_end=block.page,
                    question_type="unknown",
                    question=text      # includes the question number and the full line
                )

                qid += 1

                continue

            if current is None:

                continue

            current.question += text + "\n"

            current.page_end = block.page

        if current:

            questions.append(current)

        return questions   # clean ending, no extra code