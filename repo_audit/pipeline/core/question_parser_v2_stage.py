from pipeline.core.stage import Stage

from pipeline.layout.line_extractor import LineExtractor
from pipeline.question_splitter.line_grouper import LineGrouper
from pipeline.question_parser_v2.parser import QuestionParserV2


class QuestionParserV2Stage(Stage):

    def run(self, context):

        if context.metadata.get("skip"):
            return context

        questions = []

        sections = context.metadata.get("sections", [])

        for section in sections:

            lines = LineExtractor().extract(
                section.blocks
            )

            groups = LineGrouper().group(
                lines
            )

            qs = QuestionParserV2().parse(
                groups=groups,
                section=section,
                pdf=context.pdf,
            )

            questions.extend(qs)

        context.questions = questions

        context.metrics["questions"] = len(
            questions
        )

        return context
