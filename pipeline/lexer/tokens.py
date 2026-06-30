from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto


class TokenType(Enum):

    QUESTION_START = auto()
    STAR_QUESTION = auto()

    ROMAN = auto()
    ALPHA = auto()

    EXERCISE = auto()
    EXAMPLE = auto()
    ACTIVITY = auto()
    FIGURE_IT_OUT = auto()
    SAMPLE_QUESTION = auto()

    TABLE = auto()
    FIGURE = auto()

    TEXT = auto()


@dataclass(slots=True)
class Token:

    type: TokenType
    value: str
    start: int
    end: int
