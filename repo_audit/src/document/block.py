from dataclasses import dataclass


@dataclass
class Block:

    block_id: int

    block_type: str

    text: str

    page: int

    bbox: list
