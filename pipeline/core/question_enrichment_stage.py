from pipeline.core.stage import Stage
from pipeline.enricher import QuestionEnricher


class QuestionEnrichmentStage(Stage):

    def __init__(self):

        self.enricher = QuestionEnricher()

    def run(self, context):

        print("=" * 80)
        print("BEFORE ENRICHMENT")
        print("Questions:", len(context.questions))
        print("Max length:", max(len(q.question) for q in context.questions))
        print("Object id:", id(context.questions))

        context.questions = self.enricher.process(context.questions)

        print("=" * 80)
        print("AFTER ENRICHMENT")
        print("Questions:", len(context.questions))
        print("Max length:", max(len(q.question) for q in context.questions))
        print("Object id:", id(context.questions))

        context.metrics["enrichment"] = len(context.questions)

        return context