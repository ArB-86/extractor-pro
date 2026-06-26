from __future__ import annotations

import re

from models.question import Question


# Match standalone question numbers like "1.", "10.", "23." even when followed by text.
# Examples:
#   "1."            ?
#   "1. Graphically" ?
#   "7. If the lines" ?
# Does NOT match:
#   "0.6"           ?
#   "x=1.2"         ?
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
                # Start a new question
                if current:
                    questions.append(current)

                current = Question(
                    id=int(m.group(1)),
                    source="NCERT Exemplar",
                    chapter=self.section.title,
                    page_start=block.page,
                    page_end=block.page,
                    question_type="unknown",
                    question=text   # preserves the number and any following text
                )
                continue

            # Not a question start – append to the current question if it exists
            if current:
                current.question += "\n" + text
                current.page_end = block.page

        if current:
            questions.append(current)

        return questions