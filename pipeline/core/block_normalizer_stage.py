from pipeline.core.stage import Stage
from pipeline.block_normalizer import BlockNormalizer


class BlockNormalizerStage(Stage):

    def run(self, context):

        context.blocks = BlockNormalizer(
            context.blocks
        ).process()

        return context
