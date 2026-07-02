from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class LayoutNode:

    id: int

    page: int

    text: str

    bbox: tuple

    raw: dict

    prev: int | None = None

    next: int | None = None

    metadata: dict = field(default_factory=dict)

    @property
    def x(self):
        return self.bbox[0]

    @property
    def y(self):
        return self.bbox[1]
