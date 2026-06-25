from __future__ import annotations

from dataclasses import dataclass
from typing import List

from parsers.pdf_parser import Paragraph


class ParagraphBuilder:

    """
    Merge PDF blocks into logical paragraphs.
    """

    def __init__(self, blocks: List[Paragraph]):

        self.blocks = blocks

    def build(self):

        paragraphs = []

        current = None

        for block in self.blocks:

            text = block.text.strip()

            if not text:
                continue

            # Ignore page numbers
            if text.isdigit():
                continue

            # Ignore dates like 03/05/18
            if "/" in text and len(text) <= 10:
                continue

            if current is None:

                current = Paragraph(
                    page=block.page,
                    text=text,
                    bbox=block.bbox
                )

                continue

            # Large vertical gap -> new paragraph
            gap = block.bbox[1] - current.bbox[3]

            if block.page != current.page or gap > 12:

                paragraphs.append(current)

                current = Paragraph(
                    page=block.page,
                    text=text,
                    bbox=block.bbox
                )

            else:

                current.text += "\n" + text

                current.bbox = (

                    min(current.bbox[0], block.bbox[0]),

                    min(current.bbox[1], block.bbox[1]),

                    max(current.bbox[2], block.bbox[2]),

                    max(current.bbox[3], block.bbox[3])

                )

        if current:

            paragraphs.append(current)

        return paragraphs
