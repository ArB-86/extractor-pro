from pipeline.core.stage import Stage
from pipeline.question_parser import QuestionParser

class QuestionParserStage(Stage):

    def run(self, context):

        questions = []

        for section in context.metadata["sections"]:

            questions.extend(

                QuestionParser(section).parse()

            )

        context.questions = questions

        return context
