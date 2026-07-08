from __future__ import annotations

import copy
import re
from dataclasses import dataclass
from enum import Enum, auto
from typing import List


class HeaderType(Enum):
    EXERCISE = auto()
    EXAMPLE = auto()
    ACTIVITY = auto()
    FIGURE_IT_OUT = auto()
    SAMPLE_QUESTION = auto()
    SHORT_ANSWER = auto()
    LONG_ANSWER = auto()
    SECTION = auto()
    NONE = auto()


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

# Section number headers like "4.2 Visualising Solids"
SECTION_NUMBER = re.compile(
    r"^\d+\.\d+\s+[A-Z][A-Za-z]",
    re.I,
)

# Only known structural titles
KNOWN_SECTION_TITLES = {
    "Build it in Your Imagination",
    "Making Solids",
    "Practical Aspects of Using a Net",
    "Shortest Paths on a Cube",
    "Representation of Solids on a Plane Surface",
    "Isometric Projections",
    "Drawing on Isometric Grids",
    "Projections",
    "Fractals in Art",
    "Koch Snowflake",
    "Shadows",
    "Historical Note",
    "Summary",
    "SUMMARY",
}

_SECTION_OPENERS = {
    HeaderType.EXERCISE,
    HeaderType.FIGURE_IT_OUT,
    HeaderType.ACTIVITY,
    HeaderType.SECTION,
}

_SECTION_CLOSERS = {
    HeaderType.EXAMPLE,
    HeaderType.SAMPLE_QUESTION,
    HeaderType.SHORT_ANSWER,
    HeaderType.LONG_ANSWER,
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


def _classify_header_text(text: str) -> HeaderType:
    compact = _normalize_header_text(text)

    if not compact:
        return HeaderType.NONE

    if _EXERCISE_HEADER.match(compact):
        return HeaderType.EXERCISE

    if _EXAMPLE_HEADER.match(compact):
        return HeaderType.EXAMPLE

    if _ACTIVITY_HEADER.match(compact):
        return HeaderType.ACTIVITY

    if _FIGURE_IT_OUT.match(compact):
        return HeaderType.FIGURE_IT_OUT

    if _SAMPLE_QUESTION_HEADER.match(compact):
        return HeaderType.SAMPLE_QUESTION

    if _SHORT_ANSWER_HEADER.match(compact):
        return HeaderType.SHORT_ANSWER

    if _LONG_ANSWER_HEADER.match(compact):
        return HeaderType.LONG_ANSWER

    # Check for section number patterns like "4.2 Visualising Solids"
    line = compact.strip().splitlines()[0].strip()

    # Case-insensitive checks for common section headers
    line_norm = line.strip().casefold()

    if line_norm in {
        "summary",
        "historical note",
    }:
        return HeaderType.SECTION

    # Numbered chapter sections
    if SECTION_NUMBER.match(line):
        return HeaderType.SECTION

    # Only known structural titles
    if line in KNOWN_SECTION_TITLES:
        return HeaderType.SECTION

    return HeaderType.NONE


def is_section_start(text: str) -> bool:
    return _classify_header_text(text) in _SECTION_OPENERS


def is_section_stop(text: str) -> bool:
    return _classify_header_text(text) in _SECTION_CLOSERS


class SectionParser:

    def __init__(self, blocks):

        self.blocks = blocks

    def _classify_header(self, text: str) -> HeaderType:
        return _classify_header_text(text)

    def parse(self) -> List[Section]:

        sections: list[Section] = []
        current: Section | None = None

        for block in self.blocks:

            text = block.text.strip()

            if not text:
                continue
            print("BLOCK:", repr(text[:120]))

            first = _first_line(text)
            print("TYPE :", _classify_header_text(first))

            if text.startswith("Koch Snowflake"):
                print("BLOCK:", repr(text))
                print("TYPE :", _classify_header_text(first))

            if (
                len(text.splitlines()) > 1
                and _classify_header_text(first) == HeaderType.SECTION
            ):

                if current is not None:
                    sections.append(current)

                current = Section(
                    title=compact_section_title(first),
                    page_start=block.page,
                    page_end=block.page,
                    blocks=[],
                )

                body = "\n".join(text.splitlines()[1:]).strip()

                if body:
                    b = copy.copy(block)
                    b.text = body
                    current.blocks.append(b)

                continue

            header_type = self._classify_header(text)

            if header_type in {
                HeaderType.EXERCISE,
                HeaderType.FIGURE_IT_OUT,
                HeaderType.ACTIVITY,
                HeaderType.SECTION,
            }:

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