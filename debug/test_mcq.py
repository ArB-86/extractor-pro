from parsers.pdf_parser import PDFParser
from pipeline.block_splitter import BlockSplitter
from pipeline.layout_cleaner import LayoutCleaner
from pipeline.section_parser import SectionParser
from pipeline.question_parser import QuestionParser
from pipeline.mcq_parser import MCQParser

PDF = "/home/jiitcah.05/nlp_research_module/datasets/exemplar_raw/10th_maths/jeep203.pdf"

blocks = PDFParser(PDF).extract()
blocks = BlockSplitter(blocks).process()
blocks = LayoutCleaner(blocks).process()

sections = SectionParser(blocks).parse()

questions = QuestionParser(sections[0]).parse()

parser = MCQParser()

for q in questions[:5]:

    print("=" * 80)
    print(q.id)

    opts = parser.parse(q.question)

    for k, v in opts.items():
        print(k, ":", v)
