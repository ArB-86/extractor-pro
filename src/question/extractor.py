from src.document.document import Document
from src.document.question import Question

from src.question.segmenter import QuestionSegmenter
from src.question.merger import QuestionMerger
from src.question.models import QuestionType
from src.question.patterns import (
    MCQ_PATTERN,
    TRUE_FALSE_PATTERN,
    ASSERTION_PATTERN,
    FILL_PATTERN,
    CASE_STUDY_PATTERN,
    PROOF_PATTERN,
    CONSTRUCTION_PATTERN,
    HOTS_PATTERN,
    ACTIVITY_PATTERN,
)


class QuestionExtractor:

    def __init__(self):

        self.segmenter = QuestionSegmenter()

        self.merger = QuestionMerger()

    def _classify(self, text: str) -> QuestionType:

        if MCQ_PATTERN.search(text):
            return QuestionType.MCQ

        if TRUE_FALSE_PATTERN.search(text):
            return QuestionType.TRUE_FALSE

        if ASSERTION_PATTERN.search(text):
            return QuestionType.ASSERTION_REASON

        if FILL_PATTERN.search(text):
            return QuestionType.FILL

        if CASE_STUDY_PATTERN.search(text):
            return QuestionType.CASE_STUDY

        if PROOF_PATTERN.search(text):
            return QuestionType.PROOF

        if CONSTRUCTION_PATTERN.search(text):
            return QuestionType.CONSTRUCTION

        if HOTS_PATTERN.search(text):
            return QuestionType.HOTS

        if ACTIVITY_PATTERN.search(text):
            return QuestionType.ACTIVITY

        return QuestionType.SHORT

    def extract(
        self,
        document: Document,
    ) -> list[Question]:

        candidates = self.segmenter.segment(document)

        candidates = self.merger.merge(candidates)

        questions = []

        for c in candidates:

            questions.append(
                Question(
                    question_text=c.text,
                    chapter=c.context.chapter,
                    exercise=c.context.exercise,
                    question_number=c.number,
                    question_type=self._classify(c.text).value,
                    confidence=c.confidence,
                )
            )

        return questions
