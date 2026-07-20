from __future__ import annotations

from dataclasses import dataclass

from .line import ParsedLine


@dataclass(slots=True)
class QuestionSegment:
    lines: list[ParsedLine]
