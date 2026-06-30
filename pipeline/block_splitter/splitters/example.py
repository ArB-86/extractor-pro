from __future__ import annotations

from typing import Any, List

from ..base import BaseSplitter


class ExampleSplitter(BaseSplitter):

    name = "example"

    priority = 350

    def split(self, blocks: List[Any]) -> List[Any]:
        return blocks
