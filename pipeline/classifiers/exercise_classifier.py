from __future__ import annotations

import re

from pipeline.models import BlockType


EXERCISE_RE = re.compile(
    r'^Exercise\s+\d+(\.\d+)?',
    re.I,
)


class ExerciseClassifier:

    def classify(self, blocks):

        for block in blocks:

            if EXERCISE_RE.match(block.text):
                block.block_type = BlockType.EXERCISE

        return blocks
