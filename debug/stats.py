from collections import Counter
from pipeline.block_splitter import BlockSplitter
from parsers.pdf_parser import PDFParser
from pipeline.section_parser import SectionParser
from pipeline.question_parser import QuestionParser
from pipeline.layout_cleaner import LayoutCleaner

PDF = "/home/jiitcah.05/nlp_research_module/datasets/exemplar_raw/10th_maths/jeep203.pdf"

blocks = PDFParser(PDF).extract()

blocks = BlockSplitter(blocks).process()

blocks = LayoutCleaner(blocks).process()

print("=" * 80)
print("SECTION SUMMARY")
print("=" * 80)

total = 0

for section in sections:

    questions = QuestionParser(section).parse()

    total += len(questions)

    print(f"{section.title:20} -> {len(questions):3d} questions")

print("=" * 80)
print("TOTAL:", total)
