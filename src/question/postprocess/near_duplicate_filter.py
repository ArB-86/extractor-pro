from __future__ import annotations

import re
from collections import defaultdict

from rapidfuzz import fuzz

from src.document.question import Question


class NearDuplicateFilter:

    SIMILARITY = 95.0

    def __init__(self):
        self.index = defaultdict(list)

    @staticmethod
    def normalize(text: str) -> str:
        text = text.lower()

        # Remove question number prefix
        text = re.sub(
            r"^(?:q\.?\s*)?\d+[.)]?\s*",
            "",
            text,
        )

        # Remove isolated single letters (OCR noise)
        text = re.sub(r"\b([a-z])\b", " ", text)

        # Collapse whitespace
        text = re.sub(r"\s+", " ", text)

        # Remove punctuation except word characters
        text = re.sub(r"[^\w ]", "", text)

        return text.strip()

    @staticmethod
    def quality(q: Question) -> int:
        score = len(q.question_text)

        if q.answer:
            score += len(q.answer)

        if q.solution:
            score += len(q.solution)

        return score

    def process(
        self,
        questions: list[Question],
    ) -> list[Question]:

        kept = []
        self.index.clear()

        for q in questions:

            duplicate = False

            norm = self.normalize(
                q.question_text,
            )

            # Bucket key: same question number, similar length
            bucket_key = (
                q.question_number,
                len(norm.split()) // 5,  # group by word count bands of 5
            )

            # Check only candidates in the same bucket
            for prev in self.index.get(bucket_key, []):

                prev_norm = self.normalize(prev.question_text)

                ratio = fuzz.ratio(norm, prev_norm)
                token = fuzz.token_set_ratio(norm, prev_norm)

                score = max(ratio, token)

                print(
                    "[DUP]",
                    q.question_number,
                    f"ratio={ratio:.1f}",
                    f"token={token:.1f}",
                )

                if score < self.SIMILARITY:
                    continue

                if self.quality(q) > self.quality(prev):

                    print("=" * 80)
                    print("NEAR DUPLICATE REPLACE")
                    print("Similarity :", score)
                    print("Old :", prev.question_number)
                    print("New :", q.question_number)
                    print("=" * 80)

                    duplicate = True
                    break

                else:

                    print("=" * 80)
                    print("NEAR DUPLICATE DROP")
                    print("Similarity :", score)
                    print("Question :", q.question_number)
                    print("=" * 80)

                duplicate = True
                break

            if not duplicate:
                print(
                    "[KEEP]",
                    q.question_number,
                    q.chapter,
                )
                kept.append(q)
                self.index[bucket_key].append(q)

        return kept
