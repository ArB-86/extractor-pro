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
    r"EXERCISE\s+\S"
    r"|\d+\.\d+\s+EXERCISE\b"
    r")",
    re.I,
)

_EXEMPLAR_SECTION = re.compile(
    r"^\([A-E]\)\s*"
    r"(?:Multiple Choice|Short Answer|Long Answer|Exercise"
    r"|Short\s+Answer\s+Type|Long\s+Answer\s+Type)",
    re.I,
)

_FIGURE_IT_OUT = re.compile(r"^FIGURE\s+IT\s+OUT", re.I)

_SECTION_STOP = re.compile(
    r"^(?:"
    r"Sample Question\s*\d*"
    r"|Solution\s*:?"
    r"|Hints?\s+to\s+Selected\s+Problems"
    r"|Answers?\s+to\s+Selected\s+Problems"
    r")",
    re.I,
)


def compact_section_title(text: str) -> str:
    compact = re.sub(r"\s+", " ", text.strip())
    if len(compact) > 120:
        return compact[:120]
    return compact


def _first_line(text: str) -> str:
    return text.strip().split("\n")[0].strip()


def is_section_start(text: str) -> bool:
    if not text.strip():
        return False

    compact = re.sub(r"\s+", " ", text.strip())

    return bool(
        re.search(r"\bEXERCISE\s+\S", compact, re.I)
        or re.match(r"^\d+\.\d+\s+EXERCISE\b", compact, re.I)
        or _EXEMPLAR_SECTION.search(compact)
        or _FIGURE_IT_OUT.search(compact)
        or re.search(r"\([A-E]\)\s*Exercise", compact, re.I)
    )


def is_section_stop(text: str) -> bool:
    compact = re.sub(r"\s+", " ", text.strip())
    if not compact:
        return False
    if _SECTION_STOP.search(compact):
        return True
    if re.search(
        r"\([D-E]\)\s*(?:Activities|Activity|Short Answer|Long Answer)",
        compact,
        re.I,
    ):
        return True
    return False


class SectionParser:

    def __init__(self, blocks):

        self.blocks = blocks

    def parse(self) -> List[Section]:

        sections: list[Section] = []
        current: Section | None = None

        for block in self.blocks:

            text = block.text.strip()

            if not text:
                continue

            if is_section_start(text):

                if current is not None:
                    sections.append(current)

                current = Section(
                    title=compact_section_title(text),
                    page_start=block.page,
                    page_end=block.page,
                    blocks=[],
                )
                continue

            if current is not None and is_section_stop(text):

                sections.append(current)
                current = None
                continue

            if current is not None:

                current.blocks.append(block)
                current.page_end = block.page

        if current is not None:
            sections.append(current)

        return sections
