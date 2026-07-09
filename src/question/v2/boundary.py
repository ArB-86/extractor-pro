import re

from src.question.v2.state import ParserState


class BoundaryDetector:

    CONTINUATION_PREFIX = (
        "therefore",
        "hence",
        "thus",
        "so",
        "if",
        "then",
        "where",
        "when",
        "find",
        "calculate",
        "determine",
        "show that",
    )



    OPTION = re.compile(
        r"^\s*\([A-D]\)",
        re.IGNORECASE,
    )


    QUESTION_START = re.compile(
        r"^\s*(?:Q(?:uestion)?\s*)?\d+(?:\.\d+)?[.)]?\s+",
        re.IGNORECASE,
    )

    EXERCISE = re.compile(
        r"^\s*exercise\s+\d+(\.\d+)*",
        re.IGNORECASE,
    )

    CHAPTER = re.compile(
        r"^\s*chapter\s+\d+",
        re.IGNORECASE,
    )

    EXAMPLE = re.compile(
        r"^\s*example",
        re.IGNORECASE,
    )

    ACTIVITY = re.compile(
        r"^\s*activity",
        re.IGNORECASE,
    )

    FIGURE_IT_OUT = re.compile(
        r"figure\s+it\s+out",
        re.IGNORECASE,
    )

    SUMMARY = re.compile(
        r"^\s*summary",
        re.IGNORECASE,
    )

    def is_new_question(
        self,
        text: str,
        state: ParserState,
    ) -> bool:

        if self.OPTION.match(text):
            return False

        if self.CHAPTER.match(text):
            return False

        if self.EXERCISE.match(text):
            return False

        if self.EXAMPLE.match(text):
            return False

        if self.ACTIVITY.match(text):
            return False

        if self.FIGURE_IT_OUT.search(text):
            return False

        if self.SUMMARY.match(text):
            return False

        return bool(
            self.QUESTION_START.match(text)
        )

    def is_continuation(
        self,
        text: str,
    ) -> bool:

        if self.OPTION.match(text):
            return True

        if text.strip().startswith(("•","-","*")):
            return True

        if re.match(r"^\([ivxlcdm]+\)", text, re.I):
            return True

        lower = text.strip().lower()

        if lower.startswith(self.CONTINUATION_PREFIX):
            return True

        if lower.endswith(":"):
            return True

        if lower.startswith(("(", "[", "{")):
            return True

        return not self.QUESTION_START.match(text)
