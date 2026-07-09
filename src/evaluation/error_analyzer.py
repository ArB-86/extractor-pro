from __future__ import annotations

from dataclasses import dataclass
from collections import Counter

from src.document.question import Question


@dataclass(slots=True)
class ErrorSummary:
    false_positives: list[Question]
    false_negatives: list[object]
    top_error_tags: list[tuple[str, int]]


class ErrorAnalyzer:
    def analyze(self, predicted: list[Question], gold: list[object], matched_pairs: list[tuple[Question, object]]) -> ErrorSummary:
        matched_pred_ids = {id(p) for p, _ in matched_pairs}
        matched_gold_ids = {id(g) for _, g in matched_pairs}

        false_positives = [p for p in predicted if id(p) not in matched_pred_ids]
        false_negatives = [g for g in gold if id(g) not in matched_gold_ids]

        tags = Counter()
        for p in false_positives:
            tags["unmatched_prediction"] += 1
            if len((p.question_text or "").split()) < 5:
                tags["too_short"] += 1
            if not getattr(p, "chapter", None):
                tags["missing_chapter"] += 1

        for g in false_negatives:
            tags["missed_gold"] += 1
            if not getattr(g, "chapter", None):
                tags["gold_missing_chapter"] += 1

        return ErrorSummary(
            false_positives=false_positives,
            false_negatives=false_negatives,
            top_error_tags=tags.most_common(),
        )
