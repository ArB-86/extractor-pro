from pipeline.classifiers.question_type import QuestionTypeClassifier
from pipeline.classifiers.difficulty import DifficultyClassifier
from pipeline.classifiers.topic import TopicClassifier
from pipeline.extractors.answer_extractor import AnswerExtractor
from pipeline.extractors.solution_extractor import SolutionExtractor
from pipeline.math.formula_merger import FormulaMerger


class QuestionEnricher:

    def __init__(self):
        self.formula_merger = FormulaMerger()
        self.question_type_classifier = QuestionTypeClassifier()
        self.difficulty_classifier = DifficultyClassifier()
        self.topic_classifier = TopicClassifier()
        self.answer_extractor = AnswerExtractor()
        self.solution_extractor = SolutionExtractor()

    def process(self, questions):

        for q in questions:

            q.question = self.formula_merger.merge(q.question)

            q.question_type = (
                self.question_type_classifier.classify(q)
            )

            q.difficulty = (
                self.difficulty_classifier.classify(q)
            )

            q.topic = (
                self.topic_classifier.classify(q)
            )

            if not q.answer:
                q.answer = self.answer_extractor.extract(q.question)

            if not q.solution:
                q.solution = self.solution_extractor.extract(q.question)

        return questions