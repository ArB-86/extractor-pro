from __future__ import annotations

import re
from enum import Enum, auto


class HeadingType(Enum):
    CHAPTER = auto()
    SECTION = auto()
    EXERCISE = auto()
    SUMMARY = auto()
    TABLE = auto()
    PAGE = auto()
    FIGURE = auto()
    UNKNOWN = auto()


class HeadingClassifier:

    TABLE = re.compile(r"^table\s+\d+", re.I)

    FIGURE = re.compile(
        r"^(figure|fig\.?|figure\s+it\s+out)",
        re.I,
    )

    SUMMARY = re.compile(
        r"summary|umm\s*2\s*r\s*y|ummary",
        re.I,
    )

    PAGE = re.compile(
        r"(page\s*no|d\s*age|\bage\b)",
        re.I,
    )

    EXERCISE = re.compile(
        r"^exercise\b",
        re.I,
    )

    SECTION = re.compile(
        r"""
        ^
        (?:
            [A-Za-z ]+
        )?
        \s*
        \d+(?:\.\d+)+
        \s+
        """,
        re.X,
    )

    CHAPTER = re.compile(
        r"^chapter\s+\d+",
        re.I,
    )

    def classify(self, text: str) -> HeadingType:

        t = " ".join(text.split())

        if self.TABLE.match(t):
            return HeadingType.TABLE

        if self.PAGE.search(t):
            return HeadingType.PAGE

        if self.SUMMARY.search(t):
            return HeadingType.SUMMARY

        if self.FIGURE.match(t):
            return HeadingType.FIGURE

        if self.EXERCISE.match(t):
            return HeadingType.EXERCISE

        if self.CHAPTER.match(t):
            return HeadingType.CHAPTER

        if self.SECTION.match(t):
            return HeadingType.SECTION

        return HeadingType.UNKNOWN
