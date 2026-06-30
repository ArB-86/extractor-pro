from __future__ import annotations

from typing import Any, List

from ..base import BaseSplitter


class ActivitySplitter(BaseSplitter):

    def split(self, blocks: List[Any]) -> List[Any]:
        return blocks
