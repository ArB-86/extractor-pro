from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class LayoutLine:

    page: int
    text: str
    bbox: tuple[float, float, float, float]

    raw: dict
    block_id: str

    font_name: str = ""
    font_size: float = 0.0
    flags: int = 0

    is_bold: bool = False
    is_italic: bool = False

    indent: float = 0.0
    center_x: float = 0.0

    @property
    def x0(self):
        return self.bbox[0]

    @property
    def y0(self):
        return self.bbox[1]

    @property
    def x1(self):
        return self.bbox[2]

    @property
    def y1(self):
        return self.bbox[3]

    @property
    def width(self):
        return self.x1 - self.x0

    @property
    def height(self):
        return self.y1 - self.y0