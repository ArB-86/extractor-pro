from pipeline.core.stage import Stage
from pipeline.layout_cleaner import LayoutCleaner

class LayoutCleanerStage(Stage):

    def run(self, context):

        context.blocks = LayoutCleaner(
            context.blocks
        ).process()

        return context
