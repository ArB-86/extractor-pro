from pipeline.core.stage import Stage

from pipeline.layout.line_extractor import LineExtractor
from pipeline.question_parser_v2.exercise_tracker import ExerciseTracker
from pipeline.question_parser_v3.parser import QuestionParserV3


class QuestionParserV3Stage(Stage):

    def run(self, context):

        if context.metadata.get("skip"):
            return context

        tracker = ExerciseTracker()

        lines = LineExtractor().extract(context.blocks)

        context.questions = QuestionParserV3().parse(
            lines=lines,
            tracker=tracker,
            pdf=context.pdf,
        )

        context.metrics["questions"] = len(context.questions)

        return context
