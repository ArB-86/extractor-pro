import re

from src.question.v2.state import ParserState


class BoundaryDetector:

    QUESTION_START = re.compile(
        r"^\s*\d+[.)]\s+"
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

        return not self.QUESTION_START.match(text)
