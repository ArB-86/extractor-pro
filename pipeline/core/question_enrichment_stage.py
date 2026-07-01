from pipeline.core.stage import Stage
class QuestionEnrichmentStage(Stage):
    def run(self, context):
        if not context.questions: return context
        context.questions = [q for q in context.questions if len(q.question) > 15]
        return context
