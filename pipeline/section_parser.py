from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass(slots=True)
class Section:

    title: str
    page_start: int
    page_end: int
    blocks: list


class SectionParser:

    def __init__(self, blocks):

        self.blocks = blocks

    def parse(self) -> List[Section]:

        sections = []

        current = None

        for block in self.blocks:

            text = block.text.strip()

            upper = text.upper()

            if upper.startswith("EXERCISE"):

                if current:

                    sections.append(current)

                current = Section(
                    title=text,
                    page_start=block.page,
                    page_end=block.page,
                    blocks=[]
                )

                continue

            if current:

                current.blocks.append(block)
                current.page_end = block.page

        if current:

            sections.append(current)

        return sections
