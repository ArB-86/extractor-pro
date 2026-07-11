import re

from src.question.v2.state import ParserState


class BoundaryDetector:

    CAPTION_PATTERN = re.compile(
        r"^\s*(figure|fig\.?|table|chart|graph)\b",
        re.IGNORECASE,
    )

    ANSWER_HEADER = re.compile(
        r"^\s*(answer|answers|solution|solutions|hint|hints)\b",
        re.IGNORECASE,
    )

    SUBQUESTION = re.compile(
        r"^\s*(\([a-z]\)|\([ivxlcdm]+\)|[a-z][.)]|[ivxlcdm]+[.)])",
        re.IGNORECASE,
    )

    PAGE_NUMBER = re.compile(
        r"^\s*\d+\s*$"
    )

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

    # Updated QUESTION_START regex
    QUESTION_START = re.compile(
        r"""
        ^
        \s*
        (?:
            Question\s+
          | Q\.?\s*
        )?
        \d+
        [.)]
        \s+
        """,
        re.I | re.X,
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

        text = text.strip()

        if not text:
            return False

        # FIX: Reject answer/solution lines immediately
        if text.lower().startswith(("ans", "answer", "solution")):
            return False

        if self.CAPTION_PATTERN.match(text):
            return False

        if self.ANSWER_HEADER.match(text):
            return False

        if self.PAGE_NUMBER.match(text):
            return False

        if self.OPTION.match(text):
            return False

        if self.SUBQUESTION.match(text):
            return False

        if self.EXAMPLE.match(text):
            return False

        if self.ACTIVITY.match(text):
            return False

        if self.SUMMARY.match(text):
            return False

        if self.FIGURE_IT_OUT.search(text):
            return False

        if self.EXERCISE.match(text):
            return False

        if self.CHAPTER.match(text):
            return False

        # Section headings like "1.4 Relations..."
        if re.match(r"^\d+\.\d+\s+[A-Za-z]", text):
            return False

        # Section 1, Section 2...
        if text.lower().startswith("section"):
            return False

        # Short title blocks
        if (
            len(text.split()) <= 8
            and text == text.title()
        ):
            return False

        if self.QUESTION_START.match(text):
            return True

        if re.match(
            r"^Q\.?\d+",
            text,
            re.I,
        ):
            return True

        return False

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

        if re.match(
            r"^(use|given|let|consider|observe)\b",
            lower,
        ):
            return True

        if lower.startswith(("(", "[", "{")):
            return True

        if "|" in text:
            return True

        if "\t" in text:
            return True

        if re.search(r"\d\s+\d\s+\d", text):
            return True

        # Only one copy of each
        if text.lstrip().startswith(("i.", "ii.", "iii.", "iv.")):
            return True

        if re.match(r"^[a-z][.)]", text.strip(), re.I):
            return True

        return not self.QUESTION_START.match(text)
