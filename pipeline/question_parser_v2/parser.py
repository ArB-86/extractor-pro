from __future__ import annotations

import re

from pipeline.models.question import Question


QUESTION_NO = re.compile(r"^\*?(\d+)\.")


class QuestionParserV2:

    def parse(self, groups):

        questions = []

        for group in groups:

            lines = group.lines

            if not lines:
                continue

            first = lines[0].text.strip()

            m = QUESTION_NO.match(first)

            if not m:
                continue

            qid = int(m.group(1))

            text = "\n".join(
                line.text
                for line in lines
            ).strip()

            questions.append(
                Question(
                    id=qid,
                    source="NCERT",
                    chapter="",
                    page_start=lines[0].page,
                    page_end=lines[-1].page,
                    question=text,
                )
            )

        return questions
