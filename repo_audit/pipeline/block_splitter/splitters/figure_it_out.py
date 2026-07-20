from __future__ import annotations

from typing import Any, List

from ..base import BaseSplitter


class FigureItOutSplitter(BaseSplitter):

    name = "figure_it_out"

    priority = 370

    def split(self, blocks: List[Any]) -> List[Any]:
        return blocks
