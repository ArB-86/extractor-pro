from pipeline.core.stage import Stage

from pipeline.layout.line_extractor import LineExtractor
from pipeline.question_splitter.line_grouper import LineGrouper
from pipeline.question_parser_v2.parser import QuestionParserV2


class QuestionParserV2Stage(Stage):

    def run(self, context):

        if context.metadata.get("skip"):
            return context

        lines = LineExtractor().extract(context.blocks)

        groups = LineGrouper().group(lines)

        context.questions = QuestionParserV2().parse(groups)

        context.metrics["line_count"] = len(lines)
        context.metrics["question_groups"] = len(groups)
        context.metrics["questions"] = len(context.questions)

        return context
