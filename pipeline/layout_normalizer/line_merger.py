from __future__ import annotations

from collections import defaultdict

from pipeline.layout.line import LayoutLine


class LineMerger:

    def merge(
        self,
        lines: list[LayoutLine],
        y_threshold: float = 2.0,
    ) -> list[LayoutLine]:

        pages = defaultdict(list)

        for line in lines:
            pages[line.page].append(line)

        merged = []

        for page in sorted(pages):

            page_lines = sorted(
                pages[page],
                key=lambda x: (round(x.y0, 1), x.x0),
            )

            groups = []

            current = []

            current_y = None

            for line in page_lines:

                if current_y is None:
                    current = [line]
                    current_y = line.y0
                    continue

                if abs(line.y0 - current_y) <= y_threshold:
                    current.append(line)
                else:
                    groups.append(current)
                    current = [line]
                    current_y = line.y0

            if current:
                groups.append(current)

            for group in groups:

                group.sort(key=lambda x: x.x0)

                text = " ".join(
                    l.text.strip()
                    for l in group
                    if l.text.strip()
                )

                first = group[0]

                merged.append(
                    LayoutLine(
                        page=first.page,
                        text=text,
                        bbox=(
                            min(l.x0 for l in group),
                            min(l.y0 for l in group),
                            max(l.x1 for l in group),
                            max(l.y1 for l in group),
                        ),
                        raw=first.raw,
                        block_id=first.block_id,
                        font_name=first.font_name,
                        font_size=first.font_size,
                        flags=first.flags,
                        is_bold=first.is_bold,
                        is_italic=first.is_italic,
                        indent=first.indent,
                        center_x=first.center_x,
                    )
                )

        return merged