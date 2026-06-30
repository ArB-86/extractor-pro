from __future__ import annotations

from dataclasses import dataclass, field

from pipeline.models import Paragraph


@dataclass(slots=True)
class Node:

    block: Paragraph

    parent: "Node | None" = None

    children: list["Node"] = field(default_factory=list)

    depth: int = 0

    def add(self, child: "Node"):

        child.parent = self
        child.depth = self.depth + 1

        self.children.append(child)
