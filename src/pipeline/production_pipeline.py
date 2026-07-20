from pathlib import Path

from src.render.pdf_renderer import PDFRenderer
from src.pipeline.layout_pipeline import LayoutPipeline
from src.document.builder import DocumentBuilder
from src.pipeline.question_pipeline import QuestionPipeline
from src.dataset.master_dataset import MasterDataset
from src.pipeline.evaluation_pipeline import EvaluationPipeline


class ProductionPipeline:

    def __init__(self):
        self.renderer = PDFRenderer()
        self.layout = LayoutPipeline()
        self.questions = QuestionPipeline()
        self.evaluation = EvaluationPipeline()

    def run(
        self,
        pdf_path,
        output_dir,
        gold_path=None,
    ):
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        dataset = MasterDataset()

        pages = self.renderer.render(
            pdf_path,
            output_dir / "rendered",
        )

        all_regions = []

        for page_no, image in enumerate(pages, start=1):

            regions = self.layout.run(
                image_path=image,
                output_dir=output_dir / "layout" / f"page_{page_no:03d}",
                page=page_no,
            )

            all_regions.extend(regions)

        document = DocumentBuilder.build(all_regions)

        qs = self.questions.run(document)

        dataset.add(qs)

        result = dataset.export(
            output_dir=output_dir,
        )

        return self.evaluation.run(
            result,
            gold_path,
        )
