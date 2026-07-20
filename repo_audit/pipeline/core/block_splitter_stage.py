from pipeline.core.stage import Stage
from pipeline.block_splitter import BlockSplitter


class BlockSplitterStage(Stage):

    def run(self, context):

        splitter = BlockSplitter()
        context.blocks = splitter.split(context.blocks)

        return context
