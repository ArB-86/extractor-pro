from src.question.extractor import QuestionExtractor
from src.question.parser import QuestionParser
from src.question.classifier import QuestionClassifier
from src.question.normalizer import QuestionNormalizer
from src.question.deduplicator import QuestionDeduplicator


class QuestionPipeline:

    def __init__(self):

        self.extractor = QuestionExtractor()
        self.parser = QuestionParser()
        self.classifier = QuestionClassifier()
        self.normalizer = QuestionNormalizer()
        self.deduplicator = QuestionDeduplicator()

    def run(self, document):

        questions = self.extractor.extract(document)

        questions = self.parser.parse(questions)

        questions = self.classifier.classify(questions)

        questions = self.normalizer.normalize(questions)

        questions = self.deduplicator.deduplicate(questions)

        return questions
