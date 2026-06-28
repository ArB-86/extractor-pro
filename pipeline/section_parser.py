from __future__ import annotations

import re
from dataclasses import dataclass
from typing import List


@dataclass(slots=True)
class Section:

    title: str
    page_start: int
    page_end: int
    blocks: list


_EXERCISE_HEADER = re.compile(
    r"^(?:"
    r"(?:=\s*)?(?:\([A-E]\)\s*)?EXERCISE(?:\s+\d+(?:\.\d+)*)?"
    r"|\d+\.\d+\s+EXERCISE\b"
    r")",
    re.I,
)

_EXAMPLE_HEADER = re.compile(r"^(?:\([A-E]\)\s*)?EXAMPLE(?:\s+\d+)?\b", re.I)

_ACTIVITY_HEADER = re.compile(r"^(?:\([A-E]\)\s*)?ACTIVIT(?:Y|IES)\b", re.I)

_FIGURE_IT_OUT = re.compile(r"^FIGURE\s+IT\s+OUT", re.I)

_SAMPLE_QUESTION_HEADER = re.compile(r"^(?:\([A-E]\)\s*)?SAMPLE\s+QUESTION(?:\s+\d+)?\b", re.I)

_SHORT_ANSWER_HEADER = re.compile(
    r"^(?:\([A-E]\)\s*)?SHORT\s+ANSWER(?:\s+TYPE)?\b",
    re.I,
)

_LONG_ANSWER_HEADER = re.compile(
    r"^(?:\([A-E]\)\s*)?LONG\s+ANSWER(?:\s+TYPE)?\b",
    re.I,
)

_HEADER_TYPES = {
    "EXERCISE",
    "EXAMPLE",
    "ACTIVITY",
    "FIGURE_IT_OUT",
    "SAMPLE_QUESTION",
    "SHORT_ANSWER",
    "LONG_ANSWER",
    "NONE",
}

_SECTION_OPENERS = {"EXERCISE", "FIGURE_IT_OUT"}

_SECTION_CLOSERS = {
    "EXAMPLE",
    "ACTIVITY",
    "SAMPLE_QUESTION",
    "SHORT_ANSWER",
    "LONG_ANSWER",
}


def compact_section_title(text: str) -> str:
    compact = re.sub(r"\s+", " ", text.strip())
    if len(compact) > 120:
        return compact[:120]
    return compact


def _first_line(text: str) -> str:
    return text.strip().split("\n")[0].strip()


def _normalize_header_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip())


def _classify_header_text(text: str) -> str:
    compact = _normalize_header_text(text)

    if not compact:
        return "NONE"

    if _EXERCISE_HEADER.match(compact):
        return "EXERCISE"

    if _EXAMPLE_HEADER.match(compact):
        return "EXAMPLE"

    if _ACTIVITY_HEADER.match(compact):
        return "ACTIVITY"

    if _FIGURE_IT_OUT.match(compact):
        return "FIGURE_IT_OUT"

    if _SAMPLE_QUESTION_HEADER.match(compact):
        return "SAMPLE_QUESTION"

    if _SHORT_ANSWER_HEADER.match(compact):
        return "SHORT_ANSWER"

    if _LONG_ANSWER_HEADER.match(compact):
        return "LONG_ANSWER"

    return "NONE"


def is_section_start(text: str) -> bool:
    return _classify_header_text(text) in _SECTION_OPENERS


def is_section_stop(text: str) -> bool:
    return _classify_header_text(text) in _SECTION_CLOSERS


class SectionParser:

    def __init__(self, blocks):

        self.blocks = blocks

    def _classify_header(self, text: str) -> str:
        return _classify_header_text(text)

    def parse(self) -> List[Section]:

        sections: list[Section] = []
        current: Section | None = None

        for block in self.blocks:

            text = block.text.strip()

            if not text:
                continue

            header_type = self._classify_header(text)

            if header_type in _SECTION_OPENERS:

                if current is not None:
                    sections.append(current)

                current = Section(
                    title=compact_section_title(text),
                    page_start=block.page,
                    page_end=block.page,
                    blocks=[],
                )
                continue

            if header_type in _SECTION_CLOSERS:

                if current is not None:
                    sections.append(current)
                    current = None
                continue

            if current is not None:

                current.blocks.append(block)
                current.page_end = block.page

        if current is not None:
            sections.append(current)

        return sections
