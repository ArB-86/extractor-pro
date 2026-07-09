from src.question.extractor import QuestionExtractor
from src.question.v2.extractor import QuestionExtractorV2
from src.question.parser import QuestionParser
from src.question.classifier import QuestionClassifier
from src.question.normalizer import QuestionNormalizer
from src.question.deduplicator import QuestionDeduplicator


class QuestionPipeline:

    def __init__(
        self,
        use_v2: bool = True,
    ):

        self.extractor = (
            QuestionExtractorV2()
            if use_v2
            else QuestionExtractor()
        )

        self.parser = QuestionParser()

        self.classifier = QuestionClassifier()

        self.normalizer = QuestionNormalizer()

        self.deduplicator = QuestionDeduplicator()

    def run(self, document):

        questions = self.extractor.extract(
            document
        )

        if questions and hasattr(
            questions[0],
            "question_text",
        ):

            questions = self.parser.parse(
                questions
            )

            questions = self.classifier.classify(
                questions
            )

            questions = self.normalizer.normalize(
                questions
            )

            questions = self.deduplicator.deduplicate(
                questions
            )

            return questions

        converted = []

        from src.document.question import Question

        for q in questions:

            converted.append(
                Question(
                    question_text=q.text,
                    chapter=q.context.chapter,
                    exercise=q.context.exercise,
                    question_number=q.number,
                    question_type=q.qtype.value,
                    confidence=q.confidence,
                    metadata=q.metadata,
                )
            )

        converted = self.parser.parse(
            converted
        )

        converted = self.classifier.classify(
            converted
        )

        converted = self.normalizer.normalize(
            converted
        )

        converted = self.deduplicator.deduplicate(
            converted
        )

        return converted
