
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from pipeline.core.context import PipelineContext
from pipeline.core.engine import PipelineEngine
from pipeline.core.default_pipeline import build
from pipeline.core.report import PipelineReport
from pipeline.metadata import should_skip_pdf
from exporters.json_exporter import JSONExporter

DATASET_ROOT = Path("/home/jiitcah.05/nlp_research_module/datasets")

EXEMPLAR_DIRS = sorted((DATASET_ROOT / "exemplar_raw").glob("*_maths"))
TEXTBOOK_DIRS = sorted((DATASET_ROOT / "raw_docs").glob("*"))


def iter_pdfs():

    for folder in EXEMPLAR_DIRS:
        for pdf in sorted(folder.glob("*.pdf")):
            if should_skip_pdf(pdf):
                continue
            yield pdf

    for folder in TEXTBOOK_DIRS:
        if not folder.is_dir():
            continue
        for pdf in sorted(folder.glob("*.pdf")):
            if should_skip_pdf(pdf):
                continue
            yield pdf


def extract_pdf(pdf_path: Path, output_dir: Path):

    print("=" * 80)
    print(pdf_path)

    ctx = PipelineContext(pdf=str(pdf_path))

    engine = PipelineEngine(build())
    ctx = engine.run(ctx)

    if ctx.metadata.get("skip"):
        print("SKIPPED:", ctx.metadata.get("skip_reason", "unknown"))
        return 0

    grade = ctx.metadata.get("class")
    output_file = output_dir / f"{pdf_path.stem}.json"

    JSONExporter().export(
        ctx.questions,
        str(output_file),
        class_grade=grade,
    )

    PipelineReport().print(ctx)
    print("Output :", output_file)
    print("Questions:", len(ctx.questions))

    return len(ctx.questions)


def main():

    output_dir = PROJECT_ROOT.parent / "output" / "json"
    output_dir.mkdir(parents=True, exist_ok=True)

    pdfs = list(iter_pdfs())
    print(f"Found {len(pdfs)} PDFs")
    print()

    total_questions = 0

    for pdf in pdfs:

        try:
            total_questions += extract_pdf(pdf, output_dir)

        except Exception as e:
            print("=" * 80)
            print(pdf)
            print("FAILED:", e)

    print()
    print("TOTAL QUESTIONS:", total_questions)


if __name__ == "__main__":
    main()
