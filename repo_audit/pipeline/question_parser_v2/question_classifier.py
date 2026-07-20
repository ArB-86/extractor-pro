from __future__ import annotations

import re

from pipeline.layout.line import LayoutLine

QUESTION = "question"
CONTINUATION = "continuation"
HEADING = "heading"
OPTION = "option"
NOISE = "noise"

QUESTION_RE = re.compile(
    r"""
    ^
    (
        \d+\.
        |
        Q(?:uestion)?\s*\d+
        |
        Sample\s+Question\s+\d+
    )
    """,
    re.I | re.X,
)

_OPTION = re.compile(r"^\([A-Da-divx]+\)")
_SECTION = re.compile(r"^\d+\.\d+")
_EXERCISE = re.compile(
    r"^(EXERCISE|Miscellaneous Exercise)",
    re.I,
)

_PAGE = re.compile(r"^Reprint")
_FIG = re.compile(r"^(Fig|Figure)", re.I)


class QuestionClassifier:

    def classify(self, line: LayoutLine):

        text = line.text.strip()

        if not text:
            return NOISE

        if _PAGE.match(text):
            return NOISE

        if _FIG.match(text):
            return NOISE

        if _EXERCISE.match(text):
            return HEADING

        if _SECTION.match(text):
            return HEADING

        # New question detection logic
        m = QUESTION_RE.match(text)
        if m:
            rest = text[m.end():].strip()
            if not rest:
                return QUESTION
            if len(rest) < 2:
                return QUESTION
            return CONTINUATION

        if _OPTION.match(text):
            return OPTION

        return CONTINUATION