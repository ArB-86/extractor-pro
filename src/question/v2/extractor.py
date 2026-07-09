from __future__ import annotations

from src.document.document import Document

from src.question.v2.context import ContextManager
from src.question.v2.numbering import NumberingDetector
from src.question.v2.boundary import BoundaryDetector
from src.question.v2.assembler import QuestionAssembler
from src.question.v2.classifier import QuestionClassifier
from src.question.v2.validator import QuestionValidator
from src.question.v2.converter import CandidateConverter
from src.question.v2.postprocessor import QuestionPostProcessor
from src.question.v2.deduplicator import QuestionDeduplicatorV2


class QuestionExtractorV2:

    def __init__(self):

        self.context = ContextManager()

        self.numbering = NumberingDetector()

        self.boundary = BoundaryDetector()

        self.assembler = QuestionAssembler()

        self.classifier = QuestionClassifier()

        self.validator = QuestionValidator()
        self.converter = CandidateConverter()
        self.postprocessor = QuestionPostProcessor()
        self.deduplicator = QuestionDeduplicatorV2()

    def extract(self, document: Document):

        state = self.context.state

        for region in document.regions:

            if not region.text:
                continue

            text = region.text.strip()

            state = self.context.update(region)

            state = self.numbering.detect(
                text,
                state,
            )

            if state.inside_summary:
                continue

            if (
                state.inside_example
                or state.inside_activity
            ):
                continue

            self.assembler.consume(
                text,
                state,
            )

        questions = self.assembler.finalize()

        questions = self.classifier.classify(
            questions,
        )

        questions = self.validator.validate(
            questions,
        )

        questions = self.converter.convert(
            questions,
        )

        questions = self.postprocessor.process(
            questions,
        )

        questions = self.deduplicator.deduplicate(
            questions,
        )

        return questions
