from pathlib import Path

from parsers.pdf_parser import PDFParser
from pipeline.layout.line_extractor import LineExtractor
from pipeline.features.statistics import LayoutStatistics

pdf = Path(
    "/home/jiitcah.05/nlp_research_module/datasets/raw_docs/kemh1dd/kemh106.pdf"
)

blocks = PDFParser(str(pdf)).extract()
lines = LineExtractor().extract(blocks)

stats = LayoutStatistics().compute(lines)

print("=" * 60)
print(stats)
print("=" * 60)