from __future__ import annotations

from dataclasses import replace
from typing import List

from pipeline.models import Paragraph, BlockType

from ..base import BaseSplitter
from ..patterns import QUESTION_START


class QuestionSplitter(BaseSplitter):

    name = "question"

    priority = 500

    def split(self, blocks: List[Paragraph]) -> List[Paragraph]:

        result: List[Paragraph] = []

        for block in blocks:

            matches = list(QUESTION_START.finditer(block.text))

            if len(matches) <= 1:
                result.append(block)
                continue

            for i, match in enumerate(matches):

                start = match.start()

                if i + 1 < len(matches):
                    end = matches[i + 1].start()
                else:
                    end = len(block.text)

                text = block.text[start:end].strip()

                if not text:
                    continue

                metadata = dict(block.metadata or {})

                metadata["question_no"] = match.group("number")
                metadata["starred"] = bool(match.group("star"))

                result.append(
                    replace(
                        block,
                        text=text,
                        block_type=BlockType.QUESTION,
                        metadata=metadata,
                    )
                )

        return result
