from pipeline.core.stage import Stage
from pipeline.block_merger import BlockMerger

class BlockMergerStage(Stage):

    def run(self, context):

        context.blocks = BlockMerger(
            context.blocks
        ).process()

        return context
