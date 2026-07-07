import json

from pipeline.vision.figure_extractor import FigureExtractor
from pipeline.vision.figure_linker import FigureLinker

from parsers.pdf_parser import PDFParser
from pipeline.block_splitter import BlockSplitter
from pipeline.block_merger import BlockMerger
from pipeline.layout_cleaner import LayoutCleaner
from pipeline.section_parser import SectionParser
from pipeline.question_parser import QuestionParser

pdf = "/home/jiitcah.05/nlp_research_module/datasets/exemplar_raw/10th_maths/jeep208.pdf"

blocks = PDFParser(pdf).extract()
blocks = BlockSplitter(blocks).process()
blocks = BlockMerger(blocks).process()
blocks = LayoutCleaner(blocks).process()

sections = SectionParser(blocks).parse()

questions = []

for s in sections:
    questions.extend(QuestionParser(s).parse())

figures = FigureExtractor().extract(
    pdf,
    "output/figures"
)

questions = FigureLinker().link(
    questions,
    figures
)

for q in questions[:10]:
    print(q.id, q.page_start, q.figure)