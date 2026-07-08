from src.pdf.pdf_renderer import PDFRenderer
from src.pipeline.layout_pipeline import LayoutPipeline
from src.document.builder import DocumentBuilder
from src.dataset.builder import DatasetBuilder


class DocumentPipeline:

    def __init__(self):

        self.renderer = PDFRenderer()

        self.layout = LayoutPipeline()

        self.dataset = DatasetBuilder()

    def run(self, pdf_path, output_dir):

        pages = self.renderer.render(
            pdf_path,
            output_dir,
        )

        documents = []

        for page_no, image in enumerate(pages, start=1):

            regions = self.layout.run(
                image_path=image,
                output_dir=f"{output_dir}/page_{page_no:03d}",
                page=page_no,
            )

            doc = DocumentBuilder.build(regions)

            documents.append(doc)

        return documents
