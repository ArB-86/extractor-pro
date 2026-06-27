from __future__ import annotations

from pathlib import Path
import fitz


class FigureExtractor:

    def extract(self, pdf_path, output_dir):

        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        doc = fitz.open(pdf_path)

        figures = []

        for page_no, page in enumerate(doc):

            images = page.get_images(full=True)

            for idx, img in enumerate(images):

                xref = img[0]

                pix = fitz.Pixmap(doc, xref)

                try:
                    if pix.colorspace is None or pix.colorspace.n != 3:
                        pix = fitz.Pixmap(fitz.csRGB, pix)

                    if pix.alpha:
                        pix = fitz.Pixmap(pix, 0)

                    filename = f"page_{page_no+1:03d}_fig_{idx}.png"
                    path = output_dir / filename

                    pix.save(str(path))

                except Exception as e:
                    print(f"[WARN] page={page_no+1} image={idx} skipped: {e}")

                finally:
                    pix = None

                figures.append(
                    {
                        "page": page_no + 1,
                        "index": idx,
                        "path": str(path),
                    }
                )

        doc.close()

        return figures