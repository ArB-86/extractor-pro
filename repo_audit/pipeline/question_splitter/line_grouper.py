from __future__ import annotations

import re

from pipeline.layout.line import LayoutLine


QUESTION_START = re.compile(
    r"^\*?\d+\.\s*$|^\*?\d+\.\s+"
)


class LineGroup:
    def __init__(self):
        self.lines: list[LayoutLine] = []

    def append(self, line: LayoutLine):
        self.lines.append(line)

    @property
    def text(self):
        return "\n".join(
            line.text
            for line in self.lines
        )


class LineGrouper:

    def group(
        self,
        lines: list[LayoutLine],
    ) -> list[LineGroup]:

        groups = []

        current = None

        for line in lines:

            text = line.text.strip()

            if QUESTION_START.match(text):

                if current is not None:
                    groups.append(current)

                current = LineGroup()
                current.append(line)
                continue

            if current is not None:
                current.append(line)

        if current is not None:
            groups.append(current)

        return groups
