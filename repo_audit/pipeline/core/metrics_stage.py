
from pipeline.core.stage import Stage


class MetricsStage(Stage):

    def run(self, context):

        context.metrics["questions"] = len(
            context.questions
        )

        context.metrics["figures"] = len(
            context.figures
        )

        context.metrics["errors"] = len(
            context.errors
        )

        return context
