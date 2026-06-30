from __future__ import annotations

import re

from pipeline.models import BlockType


QUESTION_RE = re.compile(r'^\*?\d+\.\s')


class QuestionClassifier:

    def classify(self, blocks):

        for block in blocks:

            if QUESTION_RE.match(block.text):
                block.block_type = BlockType.QUESTION

        return blocks
