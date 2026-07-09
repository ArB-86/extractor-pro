import argparse
from pathlib import Path

from src.extractor.extractor import Extractor
from src.curriculum.run import CurriculumRunner
from src.pipeline.master_pipeline import MasterPipeline
from src.pdf.pdf_discovery import PDFDiscovery
from src.pipeline.scheduler import Scheduler
from src.evaluation.runner import EvaluationRunner
from src.pipeline.question_pipeline import QuestionPipeline
from src.document.builder import DocumentBuilder
from src.pipeline.layout_pipeline import LayoutPipeline
from src.pdf.pdf_renderer import PDFRenderer


def _build_document(pdf_path: str, output_dir: str):
    renderer = PDFRenderer()
    layout = LayoutPipeline()
    pages = renderer.render(pdf_path, Path(output_dir) / "render")
    all_regions = []
    for page_no, image_path in enumerate(pages, start=1):
        page_dir = Path(output_dir) / f"page_{page_no:03d}"
        regions = layout.run(image_path=image_path, output_dir=str(page_dir), page=page_no)
        all_regions.extend(regions)
    return DocumentBuilder.build(all_regions)


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    extract = sub.add_parser("extract")
    extract.add_argument("pdf")
    extract.add_argument("-o", "--output", required=True)

    curriculum = sub.add_parser("curriculum")
    curriculum.add_argument("root")
    curriculum.add_argument("-o", "--output", required=True)

    pipeline = sub.add_parser("pipeline")
    pipeline.add_argument("root")
    pipeline.add_argument("-o", "--output", required=True)

    hpc = sub.add_parser("hpc")
    hpc.add_argument("root")
    hpc.add_argument("-o", "--output", required=True)

    evaluate = sub.add_parser("evaluate")
    evaluate.add_argument("pdf")
    evaluate.add_argument("--gold", required=True)
    evaluate.add_argument("-o", "--output", required=True)

    args = parser.parse_args()

    if args.command == "extract":
        Extractor().extract(pdf_path=args.pdf, output_dir=args.output)

    elif args.command == "curriculum":
        CurriculumRunner().run(root=args.root, output=args.output)

    elif args.command == "pipeline":
        pdfs = PDFDiscovery(args.root).discover()
        MasterPipeline().run(pdfs, args.output)

    elif args.command == "hpc":
        pdfs = PDFDiscovery(args.root).discover()
        Scheduler().run(pdfs, args.output)

    elif args.command == "evaluate":
        document = _build_document(args.pdf, args.output)
        questions = QuestionPipeline().run(document)
        report = EvaluationRunner().run(questions, gold_path=args.gold, output_path=Path(args.output) / "evaluation.json")
        print(report)


if __name__ == "__main__":
    main()
