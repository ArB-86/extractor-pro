from pathlib import Path

from parsers.pdf_parser import PDFParser
from pipeline.layout.line_extractor import LineExtractor
from pipeline.question_splitter.line_grouper import LineGrouper
from pipeline.question_parser_v2.parser import QuestionParserV2

pdf = Path(
    "/home/jiitcah.05/nlp_research_module/datasets/raw_docs/kemh1dd/kemh106.pdf"
)

blocks = PDFParser(str(pdf)).extract()
lines = LineExtractor().extract(blocks)
groups = LineGrouper().group(lines)

questions = QuestionParserV2().parse(groups)

print("=" * 80)
print("Questions:", len(questions))
print("=" * 80)

for q in questions[:20]:
    print()
    print("=" * 60)
    print(f"Q{q.id}")
    print("=" * 60)
    print(q.question[:800])
