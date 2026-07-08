from pathlib import Path

import fitz


class PDFRenderer:

    def __init__(self, dpi=300):
        self.dpi = dpi

    def render(self, pdf_path: str, output_dir: str):

        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        pdf = fitz.open(pdf_path)

        pages = []

        zoom = self.dpi / 72.0

        matrix = fitz.Matrix(zoom, zoom)

        for i, page in enumerate(pdf):

            out = output_dir / f"page_{i+1:03d}.png"

            pix = page.get_pixmap(matrix=matrix, alpha=False)

            pix.save(str(out))

            pages.append(str(out))

        pdf.close()

        return pages
