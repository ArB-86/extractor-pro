from __future__ import annotations

from typing import Any, List

from ..base import BaseSplitter


class HeadingSplitter(BaseSplitter):

    name = "heading"

    priority = 100

    def split(self, blocks: List[Any]) -> List[Any]:
        return blocks
