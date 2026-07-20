from __future__ import annotations

import re
from dataclasses import dataclass


class NumberingPatterns:

    # OCR punctuation:
    # . ) ] 。 ． ﹒ ․  】 
    QUESTION_NUMBER = re.compile(
        r"""
        ^
        \s*
        (?:
            Question\s+
          |
            Q\.?\s*
        )?
        ([1-9]\d*)
        [\.\)\]】】。．﹒․]+
        \s*
        """,
        re.I | re.X,
    )

    SUBQUESTION = re.compile(
        r"""
        ^
        \s*
        (
            \([a-z]\)
            |
            \([ivxlcdm]+\)
            |
            [a-z][.)]
            |
            [ivxlcdm]+[.)]
        )
        \s+
        """,
        re.I | re.X,
    )

    OPTION = re.compile(
        r"""
        ^
        \s*
        (?:\([A-D]\)|[A-D][.)])
        \s+
        """,
        re.I | re.X,
    )


@dataclass(slots=True, frozen=True)
class NumberSignal:

    kind: str | None

    value: str | None = None


class NumberingDetector:

    _BAD_PREFIXES = (
        "table",
        "figure",
        "fig.",
        "fig ",
        "example",
        "activity",
        "note",
        "box",
        "chapter",
        "section",
        "exercise",
        "solution",
        "answer",
        "answers",
        "hint",
        "hints",
        "summary",
    )

    _BAD_REMAINDER = (
        "answer",
        "answers",
        "solution",
        "page",
        "figure",
        "table",
    )

    def read(
        self,
        text: str,
    ) -> NumberSignal:

        if not text:
            return NumberSignal(None)

        text = " ".join(text.split())

        lower = text.lower()

        if lower.startswith(self._BAD_PREFIXES):
            return NumberSignal(None)

        m = NumberingPatterns.QUESTION_NUMBER.match(text)

        if m:

            number = m.group(1)

            remainder = text[m.end():].strip()

            if not remainder:
                return NumberSignal(None)

            lower_rem = remainder.lower()

            if lower_rem.startswith(self._BAD_REMAINDER):
                return NumberSignal(None)

            if re.fullmatch(r"\d+", remainder):
                return NumberSignal(None)

            if len(remainder) < 3:
                return NumberSignal(None)

            return NumberSignal(
                kind="question",
                value=number,
            )

        if NumberingPatterns.OPTION.match(text):
            return NumberSignal("option")

        m = NumberingPatterns.SUBQUESTION.match(text)

        if m:

            return NumberSignal(
                "subquestion",
                m.group(1),
            )

        return NumberSignal(None)
