from pathlib import Path

from src.render.pdf_renderer import PDFRenderer
from src.workers.page_worker import process_page


class Extractor:

    def __init__(self):
        self.renderer = PDFRenderer()

    def extract(
        self,
        pdf_path: str,
        output_dir: str,
        workers: int = 8,
    ):
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        pages = self.renderer.render(
            pdf_path,
            output_dir / "render",
        )

        for page_no, image_path in enumerate(pages, start=1):
            process_page(
                (
                    image_path,
                    str(output_dir / f"page_{page_no:03d}"),
                    page_no,
                )
            )

        print("=" * 80)
        print("Pages:", len(pages))


        return pages
