from pathlib import Path

from src.pdf.pdf_renderer import PDFRenderer
from src.pipeline.layout_pipeline import LayoutPipeline
from src.document.builder import DocumentBuilder
from src.pipeline.question_pipeline import QuestionPipeline
from src.dataset.builder import DatasetBuilder


class DocumentPipeline:

    def __init__(self):

        self.renderer = PDFRenderer()
        self.layout = LayoutPipeline()
        self.question_pipeline = QuestionPipeline()
        self.dataset = DatasetBuilder()

    def run(self, pdf_path: str, output_dir: str):

        output_dir = Path(output_dir)

        render_dir = output_dir / "render"

        pages = self.renderer.render(
            pdf_path,
            render_dir,
        )

        for page_no, image_path in enumerate(pages, start=1):

            page_dir = output_dir / f"page_{page_no:03d}"

            regions = self.layout.run(
                image_path=image_path,
                output_dir=str(page_dir),
                page=page_no,
            )

            document = DocumentBuilder.build(regions)

            questions = self.question_pipeline.run(document)

            self.dataset.extend(questions)

        return self.dataset.build()
