from __future__ import annotations

import re

from pipeline.models import BlockType


QUESTION_RE = re.compile(
    r"^(?P<star>\*)?(?P<number>\d+)\.\s+"
)


class QuestionClassifier:

    def classify(self, blocks):

        for block in blocks:

            text = block.text.strip()

            match = QUESTION_RE.match(text)

            if match is None:
                continue

            block.block_type = BlockType.QUESTION

            block.metadata["question_no"] = int(
                match.group("number")
            )

            block.metadata["starred"] = (
                match.group("star") is not None
            )

        return blocks