from __future__ import annotations

from pipeline.layout.line import LayoutLine
from .node import LayoutNode


class LayoutGraph:

    def build(
        self,
        lines: list[LayoutLine],
    ) -> list[LayoutNode]:

        nodes = []

        for idx, line in enumerate(lines):

            node = LayoutNode(
                id=idx,
                page=line.page,
                text=line.text,
                bbox=line.bbox,
                raw=line.raw,
            )

            nodes.append(node)

        for i in range(len(nodes) - 1):

            nodes[i].next = nodes[i + 1].id

            nodes[i + 1].prev = nodes[i].id

        return nodes
