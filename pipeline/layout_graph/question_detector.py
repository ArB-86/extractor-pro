from __future__ import annotations

import re

from .node import LayoutNode


QUESTION_PATTERNS = [
    re.compile(r"^\*?\d+\.\s+"),
    re.compile(r"^\(\d+\)\s+"),
    re.compile(r"^Q\.?\s*\d+", re.I),
    re.compile(r"^Question\s+\d+", re.I),
]


class QuestionDetector:

    def detect(
        self,
        nodes: list[LayoutNode],
    ) -> list[int]:

        starts = []

        for node in nodes:

            text = node.text.strip()

            if len(text) < 2:
                continue

            if self._looks_like_question(text):
                starts.append(node.id)

        return starts

    def _looks_like_question(self, text: str) -> bool:

        for pattern in QUESTION_PATTERNS:
            if pattern.match(text):
                return True

        return False