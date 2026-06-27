
from pipeline.core.stage import Stage

from pipeline.enricher import QuestionEnricher


class EnrichmentStage(Stage):

    def __init__(self):

        self.enricher = QuestionEnricher()

    def run(self, context):

        context.questions = self.enricher.process(
            context.questions
        )

        return context


class ValidationStage(Stage):

    def run(self, context):

        # Placeholder
        return context


class AIStage(Stage):

    def run(self, context):

        # Placeholder
        return context
