from pathlib import Path

from parsers.pdf_parser import PDFParser
from pipeline.layout.line_extractor import LineExtractor

pdf = Path(
    "/home/jiitcah.05/nlp_research_module/datasets/raw_docs/kemh1dd/kemh106.pdf"
)

blocks = PDFParser(str(pdf)).extract()
lines = LineExtractor().extract(blocks)

for line in lines:
    if line.page == 8:
        print(
            f"{line.y0:7.1f} | "
            f"{line.font_size:4.1f} | "
            f"{line.is_bold} | "
            f"{line.text}"
        )
