import re
from src.question.v2.state import ParserState


class NumberingDetector:

    # FIX: Require [.)] after digits
    QUESTION = re.compile(
        r"""
        ^
        \s*
        (?:
            Question\s+
          | Q\.?\s*
        )?
        (\d+)
        [.)]
        \s+
        """,
        re.I | re.X,
    )

    SUBQUESTION = re.compile(
        r"^\s*(\([a-z]\)|\([ivxlcdm]+\)|[a-z][.)]|[ivxlcdm]+[.)])",
        re.IGNORECASE,
    )

    OPTION = re.compile(
        r"^\s*\([A-D]\)",
        re.IGNORECASE,
    )

    def detect(
        self,
        text: str,
        state: ParserState,
    ) -> ParserState:

        # FIX: Skip section titles like "1.4 Relations..."
        if re.match(r"^\d+\.\d+\s+[A-Za-z]", text):
            return state

        # Ignore option lines (they are not new questions or subquestions)
        if re.match(r"^\s*\([A-D]\)", text, re.I):
            return state

        # Try to match a main question number
        m = self.QUESTION.match(text)
        if m:
            state.question_number = m.group(1).strip()
            state.subquestion = None
            return state

        # Try to match a subquestion (a), (i), 1., etc.
        m = self.SUBQUESTION.match(text)
        if m:
            state.subquestion = m.group(1)
            return state

        # Detect if this is an option (A), (B), etc.
        if self.OPTION.match(text):
            state.metadata["option"] = True

        return state
