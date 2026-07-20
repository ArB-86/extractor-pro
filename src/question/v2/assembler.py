from __future__ import annotations

from src.question.models import (
    QuestionCandidate,
    QuestionContext,
)

from src.question.v2.boundary import LineClass
from src.question.v2.numbering import NumberSignal
from src.question.v2.state import ParserState


class QuestionAssembler:

    def __init__(self):

        self.current = None
        self.questions = []

    def _flush(self):

        if self.current:

            self.current.text = self.current.text.strip()

            if self.current.text:

                print("=" * 80)
                print("ASSEMBLER OUTPUT")
                print("PAGE :", self.current.context.page)
                print("NUM  :", self.current.number)
                print(repr(self.current.text[:300]))
                print("=" * 80)

                self.questions.append(
                    self.current
                )

        self.current = None

    def consume(
        self,
        *,
        text: str,
        state: ParserState,
        boundary: LineClass,
        signal: NumberSignal,
    ):

        text = text.strip()

        if not text:
            return

        # Header closes any open question
        if boundary == LineClass.HEADER:
            if self.current is not None:
                self._flush()
            return

        if boundary == LineClass.DROP:
            return

        if boundary == LineClass.QUESTION_START:

            if self.current is not None:
                self._flush()

            state.question_open = True
            state.question_number = signal.value

            self.current = QuestionCandidate(

                number=signal.value,

                text=text,

                context=QuestionContext(

                    chapter=state.chapter,

                    exercise=state.exercise,

                    section=state.section,

                    topic=getattr(state, "topic", None),

                    subtopic=getattr(state, "subtopic", None),

                    page=state.page,

                    source_type=state.metadata.get(
                        "source_type",
                        "textbook",
                    ),

                ),

            )

            return

        if self.current is None:
            return

        if boundary == LineClass.OPTION:

            self.current.metadata.setdefault(
                "option_count",
                0,
            )

            self.current.metadata["option_count"] += 1

            self.current.text += "\n" + text

            return

        if boundary == LineClass.SUBQUESTION:

            self.current.text += "\n" + text

            return

        if boundary == LineClass.QUESTION_BODY:

            # ---- Guard: flush on specific headings ----
            HEADINGS = (
                "note to the teacher",
                "getting a feel",
                "reading and writing",
                "creative",
                "systematic",
                "think and explore",
            )

            lower = text.lower()
            if any(lower.startswith(h) for h in HEADINGS):
                self._flush()
                return

            # Avoid duplicated OCR fragments
            if text not in self.current.text:
                self.current.text += "\n" + text

            return

    def finalize(
        self,
        state: ParserState | None = None,
    ):

        self._flush()

        if state is not None:

            state.question_open = False
            state.question_number = None

        return self.questions
