from __future__ import annotations

from .line import LayoutLine


class ReadingOrder:

    def sort(self, lines: list[LayoutLine]) -> list[LayoutLine]:

        return sorted(
            lines,
            key=lambda l: (
                l.page,
                round(l.y0, 1),
                l.x0,
            ),
        )
