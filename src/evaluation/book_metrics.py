from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class BookMetrics:
    expected_questions: int = 0
    extracted_questions: int = 0
    matched_questions: int = 0
    missed_questions: int = 0
    false_positives: int = 0
    duplicate_questions: int = 0
    expected_answers: int = 0
    extracted_answers: int = 0

    @property
    def precision(self) -> float:
        if self.extracted_questions == 0:
            return 0.0
        return self.matched_questions / self.extracted_questions

    @property
    def recall(self) -> float:
        if self.expected_questions == 0:
            return 0.0
        return self.matched_questions / self.expected_questions

    @property
    def f1(self) -> float:
        p = self.precision
        r = self.recall
        if p + r == 0:
            return 0.0
        return 2 * p * r / (p + r)
