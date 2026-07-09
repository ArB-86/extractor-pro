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
from src.question.v2.metrics import ExtractionMetrics
from src.question.v2.report import ExtractionReport
from src.question.v2.sanity import SanityChecker
from src.question.v2.debug import DebugExporter
from src.question.v2.review_queue import ReviewQueue
from src.question.v2.duplicate_detector import DuplicateDetector
from src.question.v2.debug import DebugExporter
from src.question.v2.review_queue import ReviewQueue
from src.question.v2.duplicate_detector import DuplicateDetector


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
        self.metrics = ExtractionMetrics()
        self.report = ExtractionReport()
        self.sanity = SanityChecker()
        self.debug = DebugExporter()
        self.review_queue = ReviewQueue()
        self.duplicates = DuplicateDetector()
        self.debug = DebugExporter()
        self.review_queue = ReviewQueue()
        self.duplicates = DuplicateDetector()

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

            if self.boundary.is_new_question(
                text,
                state,
            ):

                self.assembler.consume(
                    text,
                    state,
                )

                continue

            if self.boundary.is_continuation(
                text,
            ):

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

        questions = self.sanity.check(
            questions,
        )

        self.last_metrics = self.metrics.compute(
            questions,
        )

        self.last_duplicates = self.duplicates.inspect(
            questions,
        )

        self.last_review_queue = self.review_queue.build(
            questions,
        )

        return questions
