from dataclasses import dataclass


@dataclass
class Region:

    page: int

    label: str

    confidence: float

    x1: float
    y1: float
    x2: float
    y2: float

    image_path: str

    text: str | None = None