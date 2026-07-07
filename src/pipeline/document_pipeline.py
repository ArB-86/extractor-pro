from src.pdf.pdf_renderer import PDFRenderer
from src.layout.doclayout_yolo import DocLayoutYOLO
from src.ocr.qwen_cleanup import OCRCleanup
from src.dataset.builder import DatasetBuilder


class DocumentPipeline:

    def __init__(self):

        self.renderer = PDFRenderer()

        self.layout = DocLayoutYOLO()

        self.cleanup = OCRCleanup()

        self.dataset = DatasetBuilder()

    def run(self, pdf_path):

        pages = self.renderer.render(pdf_path)

        print(pages)

        return True
