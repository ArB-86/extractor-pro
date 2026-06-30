from __future__ import annotations

from typing import Any, List

from ..base import BaseSplitter


class SectionSplitter(BaseSplitter):

    name = "section"

    priority = 200

    def split(self, blocks: List[Any]) -> List[Any]:
        return blocks
