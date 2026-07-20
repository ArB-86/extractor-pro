from src.ocr.base import OCRBase


class DummyOCR(OCRBase):

    def recognize(self, image_path: str) -> str:

        return f"OCR({image_path})"
