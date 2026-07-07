from pathlib import Path

from parsers.pdf_parser import PDFParser
from pipeline.layout.line_extractor import LineExtractor
from pipeline.question_splitter.line_grouper import LineGrouper

pdf = Path(
    "/home/jiitcah.05/nlp_research_module/datasets/raw_docs/kemh1dd/kemh106.pdf"
)

blocks = PDFParser(str(pdf)).extract()

lines = LineExtractor().extract(blocks)

groups = LineGrouper().group(lines)

print("=" * 80)
print("Groups:", len(groups))
print("=" * 80)

for i, group in enumerate(groups[:20]):

    print()

    print("=" * 60)

    print("QUESTION", i + 1)

    print("=" * 60)

    print(group.text[:700])
