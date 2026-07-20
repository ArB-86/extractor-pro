from __future__ import annotations

from typing import Any, List

from ..base import BaseSplitter


class SampleQuestionSplitter(BaseSplitter):

    name = "sample_question"

    priority = 380

    def split(self, blocks: List[Any]) -> List[Any]:
        return blocks
