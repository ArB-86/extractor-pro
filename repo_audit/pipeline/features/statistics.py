from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from statistics import median

from pipeline.layout.line import LayoutLine


@dataclass(slots=True)
class DocumentStatistics:
    total_lines: int
    total_pages: int

    body_font: str
    body_font_size: float
    body_indent: float

    median_font_size: float
    largest_font_size: float
    smallest_font_size: float

    average_indent: float


class LayoutStatistics:

    def compute(self, lines: list[LayoutLine]) -> DocumentStatistics:

        if not lines:
            return DocumentStatistics(
                0, 0,
                "", 0, 0,
                0, 0, 0,
                0,
            )

        font_counter = Counter(
            (l.font_name, l.font_size)
            for l in lines
        )

        (body_font, body_size), _ = font_counter.most_common(1)[0]

        sizes = [l.font_size for l in lines]

        # Body indent: median indent of lines with body font size (within 0.1 tolerance)
        body_lines = [
            l for l in lines
            if abs(l.font_size - body_size) < 0.1
        ]

        body_indents = [l.indent for l in body_lines]

        if not body_indents:
            body_indents = [l.indent for l in lines]

        body_indent = median(body_indents)

        return DocumentStatistics(
            total_lines=len(lines),
            total_pages=max(l.page for l in lines),

            body_font=body_font,
            body_font_size=body_size,
            body_indent=body_indent,

            median_font_size=median(sizes),
            largest_font_size=max(sizes),
            smallest_font_size=min(sizes),

            average_indent=sum(body_indents) / len(body_indents),
        )