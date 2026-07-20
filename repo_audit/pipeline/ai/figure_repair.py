
from pipeline.ai.prompt import PromptManager


class FigureUnderstanding:

    def __init__(self, model):

        self.model = model
        self.prompt = PromptManager()

    def analyze(self, question, image=None):

        prompt = self.prompt.figure_understanding(question)

        return self.model.generate(
            prompt,
            image=image
        )
