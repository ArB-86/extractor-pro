from pathlib import Path

from parsers.pdf_parser import PDFParser
from pipeline.block_splitter import BlockSplitter
from pipeline.layout_cleaner import LayoutCleaner
from pipeline.document_detector import DocumentDetector

ROOT = Path(
    "/home/jiitcah.05/nlp_research_module/datasets/exemplar_raw/10th_maths"
)

detector = DocumentDetector()

for pdf in sorted(ROOT.glob("*.pdf")):

    blocks = PDFParser(str(pdf)).extract()
    blocks = BlockSplitter(blocks).process()
    blocks = LayoutCleaner(blocks).process()

    doc_type = detector.detect(blocks)

    print(f"{pdf.name:12} -> {doc_type}")
