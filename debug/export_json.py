from parsers.pdf_parser import PDFParser
from pipeline.block_splitter import BlockSplitter
from pipeline.layout_cleaner import LayoutCleaner
from pipeline.section_parser import SectionParser
from pipeline.question_parser import QuestionParser
from pipeline.enricher import QuestionEnricher
from exporters.json_exporter import JSONExporter

PDF = "/home/jiitcah.05/nlp_research_module/datasets/exemplar_raw/10th_maths/jeep203.pdf"

blocks = PDFParser(PDF).extract()
blocks = BlockSplitter(blocks).process()
blocks = LayoutCleaner(blocks).process()

sections = SectionParser(blocks).parse()

questions = []

for section in sections:
    questions.extend(
        QuestionParser(section).parse()
    )

questions = QuestionEnricher().process(questions)

JSONExporter().export(
    questions,
    "chapter3.json"
)

print("Saved", len(questions), "questions")
