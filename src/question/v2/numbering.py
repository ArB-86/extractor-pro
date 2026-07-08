import re

from src.question.v2.state import ParserState


class NumberingDetector:

    QUESTION = re.compile(
        r"^\s*(\d+)[.)]\s+"
    )

    SUBQUESTION = re.compile(
        r"^\s*\(([a-z])\)"
    )

    ROMAN = re.compile(
        r"^\s*\(([ivxlcdm]+)\)",
        re.IGNORECASE,
    )

    OPTION = re.compile(
        r"^\s*\(([A-D])\)",
        re.IGNORECASE,
    )

    def detect(
        self,
        text: str,
        state: ParserState,
    ) -> ParserState:

        if m := self.QUESTION.match(text):

            state.question_number = m.group(1)

            state.subquestion = None

            return state

        if m := self.SUBQUESTION.match(text):

            state.subquestion = m.group(1)

            return state

        if m := self.ROMAN.match(text):

            state.metadata["roman"] = m.group(1)

            return state

        if m := self.OPTION.match(text):

            state.metadata["option"] = m.group(1)

            return state

        return state
