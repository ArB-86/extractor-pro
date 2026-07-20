from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class ParsedLine:
    text: str
    spans: list
    bbox: tuple
    page: int
    line_index: int
