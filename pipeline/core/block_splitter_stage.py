from pipeline.core.stage import Stage
from pipeline.block_splitter import BlockSplitter

class BlockSplitterStage(Stage):

    def run(self, context):

        context.blocks = BlockSplitter(
            context.blocks
        ).process()

        return context
