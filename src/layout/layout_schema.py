from dataclasses import dataclass


@dataclass
class LayoutBox:

    label: str

    confidence: float

    x1: float
    y1: float
    x2: float
    y2: float
