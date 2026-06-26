from parsers.pdf_parser import PDFParser
from pipeline.block_splitter import BlockSplitter
from pipeline.section_parser import SectionParser
from pipeline.question_parser import QuestionParser

PDF = "/home/jiitcah.05/nlp_research_module/datasets/exemplar_raw/10th_maths/jeep203.pdf"

blocks = PDFParser(PDF).extract()

blocks = BlockSplitter(blocks).process()

sections = SectionParser(blocks).parse()

for section in sections:

    print("=" * 80)
    print(section.title)
    print("=" * 80)

    questions = QuestionParser(section).parse()

    for q in questions:

        first = q.question.splitlines()[0]

        print(f"{q.id:3d} | {first[:80]}")
