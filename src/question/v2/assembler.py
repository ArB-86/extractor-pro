import re


from __future__ import annotations

from src.question.models import (
    QuestionCandidate,
    QuestionContext,
)
from src.question.v2.state import ParserState


class QuestionAssembler:

    OPTION_PATTERN = re.compile(
        r"^\s*\([A-D]\)",
        re.IGNORECASE,
    )

    ROMAN_PATTERN = re.compile(
        r"^\s*\([ivxlcdm]+\)",
        re.IGNORECASE,
    )


    def __init__(self):

        self.current = None

        self.questions = []

    def consume(
        self,
        text: str,
        state: ParserState,
    ):

        text = text.strip()

        if not text:
            return

        if state.question_number:

            if (
                self.current
                and self.current.number != state.question_number
            ):

                self.questions.append(
                    self.current
                )

                self.current = None

            if self.current is None:

                cleaned = re.sub(
                    r"^\s*\d+[.)]\s+",
                    "",
                    text,
                )

                self.current = QuestionCandidate(
                    number=state.question_number,
                    text=cleaned,
                    context=QuestionContext(
                        chapter=state.chapter,
                        exercise=state.exercise,
                        page=state.page,
                    ),
                )

            else:

                if text != self.current.text:

                    self.current.text += "
" + text

        elif self.current:

            if (
                self.OPTION_PATTERN.match(text)
                or self.ROMAN_PATTERN.match(text)
                or re.match(
                    r"^\s*(\([a-z]\)|[a-z][.)])",
                    text,
                    re.I,
                )
            ):

                text = re.sub(
                    r"\s+([.,;:!?])",
                    r"\1",
                    text,
                )

                text = re.sub(
                    r"\s+([.,;:!?])",
                    r"\1",
                    text,
                )

                self.current.text += "\n" + text

                self.current.metadata.setdefault(
                    "option_count",
                    0,
                )

                self.current.metadata["option_count"] += 1

            elif self.ROMAN_PATTERN.match(text):

                self.current.text += "\n" + text

            elif (
                len(text.split()) < 4
                or len(text) < 20
            ):

                self.current.text += " " + text

            else:

                self.current.text += "\n" + text

    def finalize(self):

        if self.current:

            self.questions.append(
                self.current
            )

            self.current = None

        return self.questions
