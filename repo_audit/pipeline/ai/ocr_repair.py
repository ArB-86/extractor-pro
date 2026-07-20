
from pipeline.ai.prompt import PromptManager


class OCRRepair:

    def __init__(self, model):

        self.model = model
        self.prompt = PromptManager()

    def repair(self, text):

        prompt = self.prompt.ocr_repair(text)

        return self.model.generate(prompt)
