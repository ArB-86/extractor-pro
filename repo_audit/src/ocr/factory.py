from src.config.config import Config
from src.ocr.dummy import DummyOCR
from src.ocr.rapid_ocr import RapidOCREngine


class OCRFactory:

    _config = Config.load("ocr")

    @staticmethod
    def get(label: str):

        engine = OCRFactory._config.get(label, "dummy")

        if engine == "rapidocr":
            return RapidOCREngine()

        return DummyOCR()