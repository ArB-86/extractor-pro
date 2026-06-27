import sys
from pathlib import Path

# ------------------------------------------------------------------
# Add project root to Python path
# ------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# ------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------

from parsers.pdf_parser import PDFParser
from pipeline.block_splitter import BlockSplitter
from pipeline.block_merger import BlockMerger
from pipeline.layout_cleaner import LayoutCleaner
from pipeline.section_parser import SectionParser
from pipeline.question_parser import QuestionParser
from pipeline.enricher import QuestionEnricher
from exporters.json_exporter import JSONExporter

# ------------------------------------------------------------------
# Paths
# ------------------------------------------------------------------

INPUT_DIR = Path(
    "/home/jiitcah.05/nlp_research_module/datasets/exemplar_raw/10th_maths"
)

OUTPUT_DIR = Path("output/json")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ------------------------------------------------------------------
# Extract one PDF
# ------------------------------------------------------------------

def extract_pdf(pdf_path: Path):

    print("=" * 80)
    print(pdf_path.name)

    # ----------------------------
    # PDF -> Blocks
    # ----------------------------

    blocks = PDFParser(str(pdf_path)).extract()

    # ----------------------------
    # Pipeline
    # ----------------------------

    blocks = BlockSplitter(blocks).process()
    blocks = BlockMerger(blocks).process()
    blocks = LayoutCleaner(blocks).process()

    sections = SectionParser(blocks).parse()

    questions = []

    for section in sections:
        questions.extend(
            QuestionParser(section).parse()
        )

    questions = QuestionEnricher().process(questions)

    # ----------------------------
    # Export
    # ----------------------------

    output_file = OUTPUT_DIR / f"{pdf_path.stem}.json"

    JSONExporter().export(
        questions,
        str(output_file)
    )

    print(f"Questions : {len(questions)}")
    print(f"Output    : {output_file}")


# ------------------------------------------------------------------
# Batch extraction
# ------------------------------------------------------------------

def main():

    pdfs = sorted(INPUT_DIR.glob("*.pdf"))

    print(f"Found {len(pdfs)} PDFs\n")

    for pdf in pdfs:

        try:
            extract_pdf(pdf)

        except Exception as e:
            print("=" * 80)
            print(f"FAILED : {pdf.name}")
            print(e)


# ------------------------------------------------------------------

if __name__ == "__main__":
    main()