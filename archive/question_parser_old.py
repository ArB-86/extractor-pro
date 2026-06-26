from __future__ import annotations

import re

from models.question import Question
from pipeline.paragraph_builder import Paragraph


class QuestionParser:

    def __init__(self, paragraphs):

        self.paragraphs = paragraphs

    def parse(self):

        questions = []

        inside_exercise = False

        qid = 1

        current = None

        pattern = re.compile(r"(?m)^\s*(\d+)\.")

        for para in self.paragraphs:

            text = para.text.strip()

            if "EXERCISE" in text.upper():
                inside_exercise = True

            if not inside_exercise:
                continue

            # Split a paragraph into multiple questions
            matches = list(pattern.finditer(text))

            if not matches:

                if current:
                    current.question += "\n" + text
                    current.page_end = para.page

                continue

            for i, m in enumerate(matches):

                start = m.start()

                end = matches[i + 1].start() if i + 1 < len(matches) else len(text)

                qtext = text[start:end].strip()

                if current:
                    questions.append(current)

                current = Question(
                    id=qid,
                    source="NCERT Exemplar",
                    chapter="",
                    page_start=para.page,
                    page_end=para.page,
                    question_type="unknown",
                    question=qtext
                )

                qid += 1

        if current:
            questions.append(current)

        return questions
