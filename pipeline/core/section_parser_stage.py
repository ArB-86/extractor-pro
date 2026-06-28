from pipeline.core.stage import Stage
from pipeline.section_parser import SectionParser


class SectionParserStage(Stage):

    def run(self, context):

        if context.metadata.get("skip"):
            context.metadata["sections"] = []
            return context

        context.metadata["sections"] = SectionParser(
            context.blocks
        ).parse()

        return context
