from __future__ import annotations

import re
from collections import Counter

from pipeline.layout.line import LayoutLine


_SECTION = re.compile(r"^\d+\.\d+")
_EXERCISE = re.compile(
    r"^(EXERCISE|SUMMARY|Historical Note|Miscellaneous)",
    re.I,
)
_FIGURE = re.compile(r"^(Fig|Figure)\b", re.I)


def dominant_font(lines: list[LayoutLine]) -> tuple[str, float]:
    counter = Counter(
        (l.font_name, l.font_size)
        for l in lines
    )
    return counter.most_common(1)[0][0]


def is_bold(line: LayoutLine) -> bool:
    return line.is_bold


def is_italic(line: LayoutLine) -> bool:
    return line.is_italic


def is_large(
    line: LayoutLine,
    body_font_size: float,
    threshold: float = 1.0,
) -> bool:
    return line.font_size >= body_font_size + threshold


def is_heading(
    line: LayoutLine,
    body_font_size: float,
) -> bool:

    text = line.text.strip()

    if not text:
        return False

    alpha = sum(c.isalpha() for c in text)
    if alpha < 3:
        return False

    if re.fullmatch(r"\d+\.", text):
        return False

    if text.startswith((
        "Example",
        "Solution",
        "Definition",
        "Proof",
        "Theorem",
        "Alternative Method",
        "Remarks",
    )):
        return False

    if "Note" in text:
        return False

    if _FIGURE.match(text):
        return False

    if _EXERCISE.match(text):
        return True

    if _SECTION.match(text):
        return True

    if line.font_size >= body_font_size + 1.5:
        return True

    if (
        line.is_bold
        and len(text.split()) <= 6
        and line.font_size >= body_font_size
    ):
        return True

    return False