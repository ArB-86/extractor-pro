
from __future__ import annotations

from src.question.models import (
    QuestionCandidate,
    QuestionContext,
)
from src.question.v2.state import ParserState


class QuestionAssembler:

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

                self.current = QuestionCandidate(
                    number=state.question_number,
                    text=text,
                    context=QuestionContext(
                        chapter=state.chapter,
                        exercise=state.exercise,
                        page=state.page,
                    ),
                )

            else:

                self.current.text += "\n" + text

        elif self.current:

            self.current.text += "\n" + text

    def finalize(self):

        if self.current:

            self.questions.append(
                self.current
            )

            self.current = None

        return self.questions
