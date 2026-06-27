
from pipeline.ai.prompt import PromptManager


class FormulaRepair:

    def __init__(self, model):

        self.model = model
        self.prompt = PromptManager()

    def repair(self, formula):

        prompt = self.prompt.formula_repair(formula)

        return self.model.generate(prompt)
