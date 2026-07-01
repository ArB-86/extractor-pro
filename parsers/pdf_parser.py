import fitz
from pipeline.models import SemanticBlock, BlockType

class PDFParser:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path

    def extract(self) -> list[SemanticBlock]:
        doc = fitz.open(self.pdf_path)
        blocks = []
        for page_num, page in enumerate(doc):
            page_dict = page.get_text("dict")
            for b in page_dict.get("blocks", []):
                if b.get("type") == 0:
                    lines = b.get("lines", [])
                    if not lines:
                        continue
                    
                    text = "\n".join(
                        "".join(span.get("text", "") for span in line.get("spans", []))
                        for line in lines
                    ).strip()
                    
                    if not text:
                        continue

                    blocks.append(
                        SemanticBlock(
                            page=page_num + 1,
                            text=text,
                            bbox=tuple(b.get("bbox", (0, 0, 0, 0))),
                            raw_lines=lines,
                            block_type=BlockType.PARAGRAPH
                        )
                    )
        return blocks
