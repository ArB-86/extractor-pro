from __future__ import annotations

from typing import Any, List

from ..base import BaseSplitter


class ParagraphSplitter(BaseSplitter):

    name = "paragraph"

    priority = 900

    def split(self, blocks: List[Any]) -> List[Any]:
        return blocks
