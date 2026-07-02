from __future__ import annotations

from dataclasses import replace
from uuid import uuid4

from pipeline.models import BlockType, Paragraph
from ..base import BaseSplitter
from ..patterns import QUESTION_START


class QuestionSplitter(BaseSplitter):

    name = "question"

    priority = 500

    def split(self, blocks: list[Paragraph]) -> list[Paragraph]:

        output = []

        for block in blocks:

            if not block.raw_lines:
                output.append(block)
                continue

            segments = self._segment(block)

            if len(segments) == 1:
                output.append(block)
                continue

            output.extend(
                self._build_block(block, lines)
                for lines in segments
            )

        return output

    # ---------------------------------------------------------

    def _segment(self, block):

        segments = []

        current = []

        for line in block.raw_lines:

            text = self._line_text(line)

            if self._is_question_start(text) and current:
                segments.append(current)
                current = []

            current.append(line)

        if current:
            segments.append(current)

        return segments

    # ---------------------------------------------------------

    def _is_question_start(self, text):

        return QUESTION_START.match(text) is not None

    # ---------------------------------------------------------

    def _line_text(self, line):

        return "".join(
            span.get("text", "")
            for span in line.get("spans", [])
        ).strip()

    # ---------------------------------------------------------

    def _build_block(
        self,
        original,
        lines,
    ):

        x0 = min(
            line["bbox"][0]
            for line in lines
        )

        y0 = min(
            line["bbox"][1]
            for line in lines
        )

        x1 = max(
            line["bbox"][2]
            for line in lines
        )

        y1 = max(
            line["bbox"][3]
            for line in lines
        )

        text = "\n".join(
            self._line_text(line)
            for line in lines
        )

        metadata = dict(original.metadata)

        first = self._line_text(lines[0])

        m = QUESTION_START.match(first)

        if m:

            metadata["question_no"] = int(
                m.group("number")
            )

            metadata["starred"] = bool(
                m.group("star")
            )

        return replace(
            original,
            id=uuid4().hex,
            text=text,
            raw_lines=lines,
            bbox=(x0, y0, x1, y1),
            metadata=metadata,
            block_type=BlockType.QUESTION,
        )