
from pipeline.ai.ocr_repair import OCRRepair
from pipeline.ai.formula_repair import FormulaRepair
from pipeline.ai.figure_repair import FigureUnderstanding


class AIPipeline:

    def __init__(self, model):

        self.ocr = OCRRepair(model)
        self.formula = FormulaRepair(model)
        self.figure = FigureUnderstanding(model)
