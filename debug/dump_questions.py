from parsers.pdf_parser import PDFParser
from pipeline.paragraph_builder import ParagraphBuilder
from pipeline.question_parser import QuestionParser
from pipeline.section_parser import SectionParser   # new import

from pipeline.block_splitter import BlockSplitter



PDF = "/home/jiitcah.05/nlp_research_module/datasets/exemplar_raw/10th_maths/jeep203.pdf"

blocks = PDFParser(PDF).extract()

blocks = BlockSplitter(blocks).process()

sections = SectionParser(blocks).parse()

all_questions = []

for section in sections:
    # Each section is expected to be a list of paragraphs (or blocks)
    # that QuestionParser can handle directly.
    parser = QuestionParser(section)
    all_questions.extend(parser.parse())

with open("questions_dump.txt", "w", encoding="utf8") as f:
    for q in all_questions:
        f.write("=" * 100 + "\n")
        f.write(f"QUESTION {q.id}\n")
        f.write(f"PAGE : {q.page_start}-{q.page_end}\n\n")
        f.write(q.question)
        f.write("\n\n")

print("Saved", len(all_questions), "questions")