from dataclasses import dataclass, field

from .block import Block


@dataclass
class Page:

    page_number: int

    width: int

    height: int

    blocks: list[Block] = field(default_factory=list)
