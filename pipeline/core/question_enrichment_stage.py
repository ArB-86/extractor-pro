
from pipeline.core.stage import Stage
from pipeline.enricher import QuestionEnricher


class QuestionEnrichmentStage(Stage):

    def __init__(self):

        self.enricher = QuestionEnricher()

    def run(self, context):

        context.questions = self.enricher.process(
            context.questions
        )

        context.metrics["enrichment"] = len(context.questions)

        return context
