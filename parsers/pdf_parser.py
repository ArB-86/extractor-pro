from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import fitz


@dataclass(slots=True)
class Paragraph:

    page: int

    text: str

    bbox: tuple


class PDFParser:

    def __init__(self, pdf_path: str):

        self.path = Path(pdf_path)

        if not self.path.exists():

            raise FileNotFoundError(pdf_path)

    def extract(self):

        pdf = fitz.open(self.path)

        paragraphs = []

        for page_no, page in enumerate(pdf, start=1):

            blocks = page.get_text("blocks")

            blocks.sort(key=lambda x: (x[1], x[0]))

            for block in blocks:

                x0, y0, x1, y1, text = block[:5]

                text = text.strip()

                if not text:

                    continue

                paragraphs.append(

                    Paragraph(

                        page=page_no,

                        text=text,

                        bbox=(x0, y0, x1, y1)

                    )

                )

        pdf.close()

        return paragraphs
