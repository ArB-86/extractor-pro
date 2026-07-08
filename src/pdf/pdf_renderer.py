import fitz
from pathlib import Path


class PDFRenderer:

    def render(self, pdf_path):

        pdf_path = Path(pdf_path)

        document = fitz.open(pdf_path)

        output_dir = Path("data/rendered") / pdf_path.stem

        output_dir.mkdir(parents=True, exist_ok=True)

        pages = []

        for page_number in range(len(document)):

            page = document.load_page(page_number)

            pix = page.get_pixmap(dpi=300)

            image_path = output_dir / f"page_{page_number+1:03d}.png"

            pix.save(str(image_path))

            pages.append(str(image_path))

        document.close()

        return pages
