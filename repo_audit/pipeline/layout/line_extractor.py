from __future__ import annotations

from pipeline.layout.line import LayoutLine
from pipeline.models import Paragraph


class LineExtractor:
    """
    Converts SemanticBlocks into a document-wide list of LayoutLines.
    """

    def extract(
        self,
        blocks: list[Paragraph],
    ) -> list[LayoutLine]:

        lines: list[LayoutLine] = []

        for block in blocks:

            for raw_line in block.raw_lines:

                spans = raw_line.get("spans", [])

                text = "".join(
                    span.get("text", "")
                    for span in spans
                ).strip()

                if not text:
                    continue

                font_size = max(
                    (s.get("size", 0) for s in spans),
                    default=0,
                )

                font = (
                    spans[0].get("font", "")
                    if spans else ""
                )

                flags = (
                    spans[0].get("flags", 0)
                    if spans else 0
                )

                page_width = block.bbox[2]

                lines.append(
                    LayoutLine(
                        page=block.page,
                        text=text,
                        bbox=tuple(raw_line["bbox"]),
                        raw=raw_line,
                        block_id=block.id,

                        font_name=font,
                        font_size=font_size,
                        flags=flags,

                        is_bold=("Bold" in font) or (flags & 16 != 0),
                        is_italic=("Italic" in font) or (flags & 2 != 0),

                        indent=raw_line["bbox"][0],
                        center_x=(raw_line["bbox"][0] + raw_line["bbox"][2]) / 2,
                    )
                )

        lines.sort(
            key=lambda l: (
                l.page,
                round(l.y0, 1),
                l.x0,
            )
        )

        return lines