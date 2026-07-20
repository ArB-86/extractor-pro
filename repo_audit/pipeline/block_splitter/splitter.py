from __future__ import annotations

from pipeline.models import Paragraph

from .registry import SPLITTERS


class BlockSplitter:

    def __init__(self):

        self.splitters = [
            cls()
            for cls in sorted(
                SPLITTERS,
                key=lambda cls: cls.priority,
            )
            if cls.enabled
        ]

    def split(self, blocks: list[Paragraph]) -> list[Paragraph]:

        for splitter in self.splitters:
            blocks = splitter.split(blocks)

        return blocks
