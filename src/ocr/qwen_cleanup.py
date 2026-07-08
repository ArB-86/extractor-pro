from src.llm import QwenClient


class OCRCleanup:

    def __init__(self):

        self.llm = QwenClient()

    def clean(self, text):

        return text
