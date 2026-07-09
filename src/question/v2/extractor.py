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
from src.question.v2.quality import QualityInspector
from src.question.v2.export import QuestionExporter
from src.question.v2.context_validator import ContextValidator
from src.question.v2.number_validator import NumberValidator
from src.question.v2.confidence import ConfidenceCalibrator


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
        self.quality = QualityInspector()
        self.exporter = QuestionExporter()
        self.context_validator = ContextValidator()
        self.number_validator = NumberValidator()
        self.confidence = ConfidenceCalibrator()

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

        questions = self.quality.inspect(
            questions,
        )

        questions = self.context_validator.validate(
            questions,
        )

        questions = self.number_validator.validate(
            questions,
        )

        questions = self.confidence.calibrate(
            questions,
        )

        return questions
