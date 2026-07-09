import re

from src.question.v2.state import ParserState


class NumberingDetector:

    QUESTION = re.compile(
        r"^\s*((?:Q(?:uestion)?\s*)?\d+(?:\.\d+)?)[.)]?\s+",
        re.IGNORECASE,
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


        if re.match(r"^\s*\([A-D]\)", text, re.I):
            return state

        if m := self.QUESTION.match(text):


            number = m.group(1)

            number = re.sub(
                r"(?i)^question\s*",
                "",
                number,
            )

            number = number.rstrip(".")
            number = number.rstrip(")")
            number = number.strip()

            state.question_number = number

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
