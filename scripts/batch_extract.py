
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from pipeline.core.context import PipelineContext
from pipeline.core.engine import PipelineEngine
from pipeline.core.default_pipeline import build
from pipeline.core.report import PipelineReport
from exporters.json_exporter import JSONExporter


INPUT_DIR = Path(
    "/home/jiitcah.05/nlp_research_module/datasets/exemplar_raw/10th_maths"
)

OUTPUT_DIR = Path("output/json")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def extract_pdf(pdf_path):

    print("=" * 80)
    print(pdf_path.name)

    ctx = PipelineContext(
        pdf=str(pdf_path)
    )

    engine = PipelineEngine(
        build()
    )

    ctx = engine.run(ctx)

    output_file = OUTPUT_DIR / f"{pdf_path.stem}.json"

    JSONExporter().export(
        ctx.questions,
        str(output_file)
    )

    PipelineReport().print(ctx)

    print()

    print("Output :", output_file)


def main():

    pdfs = sorted(INPUT_DIR.glob("*.pdf"))

    print(f"Found {len(pdfs)} PDFs")

    print()

    for pdf in pdfs:

        try:

            extract_pdf(pdf)

        except Exception as e:

            print("=" * 80)

            print(pdf.name)

            print(e)


if __name__ == "__main__":

    main()
