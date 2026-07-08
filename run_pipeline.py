from src.pdf.pdf_discovery import PDFDiscovery
from src.pdf.pdf_renderer import PDFRenderer
from src.config.paths import RAW_DATASET

finder = PDFDiscovery(RAW_DATASET)

renderer = PDFRenderer()

pdfs = finder.discover()

print(f"{len(pdfs)} PDFs found")

for pdf in pdfs:

    print("=" * 80)

    print(pdf)

    pages = renderer.render(pdf)

    print(f"{len(pages)} pages rendered")
