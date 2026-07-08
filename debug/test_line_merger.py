from pathlib import Path

from parsers.pdf_parser import PDFParser
from pipeline.layout.line_extractor import LineExtractor
from pipeline.layout_normalizer.line_merger import LineMerger

pdf = Path(
    "/home/jiitcah.05/nlp_research_module/datasets/raw_docs/kemh1dd/kemh106.pdf"
)

blocks = PDFParser(str(pdf)).extract()

lines = LineExtractor().extract(blocks)

merged = LineMerger().merge(lines)

for line in merged:
    if line.page == 8:
        print(f"{line.y0:7.1f} | {line.text}")
