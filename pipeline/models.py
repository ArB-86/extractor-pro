from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from uuid import uuid4


class BlockType(Enum):

    UNKNOWN = auto()

    CHAPTER = auto()
    SECTION = auto()

    EXERCISE = auto()
    MISC_EXERCISE = auto()

    EXAMPLE = auto()
    ACTIVITY = auto()
    FIGURE_IT_OUT = auto()
    SAMPLE_QUESTION = auto()

    QUESTION = auto()
    SUBQUESTION = auto()

    TABLE = auto()
    FIGURE = auto()

    PARAGRAPH = auto()


@dataclass(slots=True)
class SemanticBlock:

    id: str = field(default_factory=lambda: uuid4().hex)

    page: int = 0

    text: str = ""

    bbox: tuple = ()

    block_type: BlockType = BlockType.UNKNOWN

    parent_id: str | None = None

    children: list[str] = field(default_factory=list)

    metadata: dict = field(default_factory=dict)


Paragraph = SemanticBlock
