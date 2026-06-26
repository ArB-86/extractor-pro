
from parsers.pdf_parser import PDFParser
from pipeline.section_parser import SectionParser

PDF = "/home/jiitcah.05/nlp_research_module/datasets/exemplar_raw/10th_maths/jeep203.pdf"

blocks = PDFParser(PDF).extract()
sections = SectionParser(blocks).parse()

section = sections[1]   # Exercise 3.2

for i, block in enumerate(section.blocks):
    print("=" * 80)
    print(i)
    print(repr(block.text))
