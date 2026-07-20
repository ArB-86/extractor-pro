import argparse
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import hashlib
import fitz
import json

SUPPORTED = {".pdf"}


class PDFLoader:

    def __init__(self, workers=8):
        self.workers = workers

    def sha256(self, path):
        h = hashlib.sha256()
        with open(path, "rb") as f:
            while True:
                b = f.read(1024 * 1024)
                if not b:
                    break
                h.update(b)
        return h.hexdigest()

    def page_info(self, page):
        return {
            "width": page.rect.width,
            "height": page.rect.height,
            "rotation": page.rotation,
            "text_blocks": len(page.get_text("blocks")),
            "images": len(page.get_images(full=True)),
        }

    def analyze_pdf(self, pdf):
        doc = fitz.open(pdf)

        with ThreadPoolExecutor(max_workers=self.workers) as exe:
            pages = list(exe.map(self.page_info, doc))

        result = {
            "file": str(pdf),
            "sha256": self.sha256(pdf),
            "pages": len(doc),
            "metadata": doc.metadata,
            "page_info": pages,
        }

        doc.close()
        return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    args = parser.parse_args()

    raw = Path(args.input)                     # <-- replaced line

    out = Path("datasets/intermediate/pdf_analysis")
    out.mkdir(parents=True, exist_ok=True)

    loader = PDFLoader()
    pdfs = sorted(raw.rglob("*.pdf"))
    print(f"Found {len(pdfs)} pdfs")

    for pdf in pdfs:
        result = loader.analyze_pdf(pdf)
        outfile = out / (pdf.stem + ".json")
        with open(outfile, "w", encoding="utf8") as f:
            json.dump(result, f, indent=2)
        print("Done", pdf.name)


if __name__ == "__main__":
    main()