from __future__ import annotations
from dataclasses import replace
from typing import List
from uuid import uuid4

from pipeline.models import Paragraph, BlockType
from ..base import BaseSplitter
from ..patterns import QUESTION_START

class QuestionSplitter(BaseSplitter):
    name = "question"
    priority = 500

    def split(self, blocks: List[Paragraph]) -> List[Paragraph]:
        result: List[Paragraph] = []

        for block in blocks:
            if not block.raw_lines:
                result.append(block)
                continue

            current_lines = []
            split_blocks = []

            for line in block.raw_lines:
                line_text = "".join(span.get("text", "") for span in line.get("spans", [])).strip()
                
                if QUESTION_START.match(line_text) and current_lines:
                    split_blocks.append(self._create_block_from_lines(block, current_lines))
                    current_lines = []
                
                current_lines.append(line)

            if current_lines:
                split_blocks.append(self._create_block_from_lines(block, current_lines))

            if len(split_blocks) == 1:
                result.append(block)
            else:
                result.extend(split_blocks)

        return result

    def _create_block_from_lines(self, original_block: Paragraph, lines: list[dict]) -> Paragraph:
        x0 = min(l["bbox"][0] for l in lines)
        y0 = min(l["bbox"][1] for l in lines)
        x1 = max(l["bbox"][2] for l in lines)
        y1 = max(l["bbox"][3] for l in lines)

        text = "\n".join(
            "".join(span.get("text", "") for span in line.get("spans", []))
            for line in lines
        ).strip()

        first_line_text = "".join(span.get("text", "") for span in lines[0].get("spans", [])).strip()
        match = QUESTION_START.match(first_line_text)
        
        metadata = dict(original_block.metadata or {})
        block_type = original_block.block_type

        if match:
            metadata["question_no"] = match.group("number")
            metadata["starred"] = bool(match.group("star"))
            block_type = BlockType.QUESTION

        return replace(
            original_block,
            id=uuid4().hex,
            text=text,
            bbox=(x0, y0, x1, y1),
            raw_lines=lines,
            block_type=block_type,
            metadata=metadata
        )
