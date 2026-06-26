from pipeline.mcq_parser import MCQParser
from pipeline.answer_parser import AnswerParser


class QuestionEnricher:

    def __init__(self):

        self.mcq = MCQParser()
        self.answer = AnswerParser()

    def process(self, questions):

        for q in questions:

            q.options = self.mcq.parse(q.question)

            q.answer = self.answer.parse(q.question)

        return questions
