from __future__ import annotations

from dataclasses import dataclass
from difflib import SequenceMatcher
from typing import Iterable

from src.document.question import Question
from src.evaluation.metrics import EvaluationMetrics
from src.evaluation.boundary import BoundaryMetrics
from src.evaluation.question_metrics import QuestionMetrics


def _normalize(text: str) -> str:
    return " ".join((text or "").strip().lower().split())


@dataclass(slots=True)
class AlignmentResult:
    question_metrics: QuestionMetrics
    boundary_metrics: BoundaryMetrics
    exact_question_matches: int
    matched_pairs: list[tuple[Question, object]]


class AlignmentEngine:
    def __init__(self, similarity_threshold: float = 0.92):
        self.similarity_threshold = similarity_threshold

    def _score(self, a: str, b: str) -> float:
        return SequenceMatcher(None, _normalize(a), _normalize(b)).ratio()

    def align(self, predicted: list[Question], gold: list[object]) -> AlignmentResult:
        matched_pairs: list[tuple[Question, object]] = []
        used_gold: set[int] = set()
        exact_matches = 0
        boundary_exact = 0
        boundary_total = min(len(predicted), len(gold))

        for p in predicted:
            best_idx = None
            best_score = 0.0
            for i, g in enumerate(gold):
                if i in used_gold:
                    continue
                score = self._score(p.question_text, getattr(g, "question_text", ""))
                if score > best_score:
                    best_score = score
                    best_idx = i
            if best_idx is not None and best_score >= self.similarity_threshold:
                used_gold.add(best_idx)
                g = gold[best_idx]
                matched_pairs.append((p, g))
                if _normalize(p.question_text) == _normalize(getattr(g, "question_text", "")):
                    exact_matches += 1
                    boundary_exact += 1
                elif self._same_boundary(p, g):
                    boundary_exact += 1

        qm = QuestionMetrics(
            total_predicted=len(predicted),
            total_gold=len(gold),
            matched=len(matched_pairs),
            exact_matches=exact_matches,
        )
        bm = BoundaryMetrics(
            exact_match=exact_matches,
            boundary_match=boundary_exact,
            total=boundary_total,
        )
        return AlignmentResult(
            question_metrics=qm,
            boundary_metrics=bm,
            exact_question_matches=exact_matches,
            matched_pairs=matched_pairs,
        )

    def _same_boundary(self, p: Question, g: object) -> bool:
        return (
            getattr(p, "chapter", None) == getattr(g, "chapter", None)
            and getattr(p, "exercise", None) == getattr(g, "exercise", None)
            and getattr(p, "question_number", None) == getattr(g, "question_number", None)
        )
