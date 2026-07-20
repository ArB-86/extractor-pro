from pipeline.math.formula_merger import FormulaMerger


class QuestionEnricher:

    def __init__(self):
        self.formula_merger = FormulaMerger()

    def process(self, questions):

        for q in questions:
            q.question = self.formula_merger.merge(q.question)

        return questions
