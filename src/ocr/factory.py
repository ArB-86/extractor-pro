from src.config.config import Config
from src.ocr.dummy import DummyOCR
from src.ocr.rapid_ocr import RapidOCREngine


class OCRFactory:

    _config = Config.load("ocr")
    _instances = {}

    @staticmethod
    def get(label: str):

        engine = OCRFactory._config.get(label, "dummy")

        if engine not in OCRFactory._instances:
            if engine == "rapidocr":
                OCRFactory._instances[engine] = RapidOCREngine()
            else:
                OCRFactory._instances[engine] = DummyOCR()

        return OCRFactory._instances[engine]
