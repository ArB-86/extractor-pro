from parsers.pdf_parser import PDFParser
from pipeline.block_splitter import BlockSplitter
from pipeline.layout_cleaner import LayoutCleaner

PDF = "/home/jiitcah.05/nlp_research_module/datasets/exemplar_raw/10th_maths/jeep214.pdf"

blocks = PDFParser(PDF).extract()
blocks = BlockSplitter(blocks).process()
blocks = LayoutCleaner(blocks).process()

print("Blocks:", len(blocks))

for i, block in enumerate(blocks[:120]):
    print("=" * 80)
    print("BLOCK", i)
    print(repr(block.text))