from __future__ import annotations

from collections import Counter, defaultdict

from pipeline.layout.line import LayoutLine


class PageStatistics:

    def compute(self, lines: list[LayoutLine]):

        pages = defaultdict(list)

        for line in lines:
            pages[line.page].append(line)

        stats = {}

        for page, page_lines in pages.items():

            indents = [
                round(l.indent)
                for l in page_lines
            ]

            body_indent = Counter(indents).most_common(1)[0][0]

            stats[page] = {
                "body_indent": float(body_indent),
                "line_count": len(page_lines),
                "left_margin": min(l.x0 for l in page_lines),
                "right_margin": max(l.x1 for l in page_lines),
            }

        return stats
