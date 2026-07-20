from __future__ import annotations

import re

from src.question.models import QuestionCandidate
from src.question.v2.text_repair import TextRepair
from src.question.v2.completeness import CompletenessScorer
from src.question.v2.sanity import QuestionSanity
from src.question.v2.quality import QuestionQuality


class QuestionValidator:
    """Validate and clean question candidates before conversion."""

    def validate(self, candidates: list[QuestionCandidate]) -> list[QuestionCandidate]:
        """Filter out invalid candidates and clean text."""
        valid = []

        for q in candidates:
            if q is None:
                continue

            # ---- Unique ID for debugging ----
            qid = f"{q.context.page}:{q.number}"
            print("=" * 80)
            print("VALIDATOR START")
            print("ID   :", qid)
            print("RAW  :", repr(q.text[:120]))
            print("=" * 80)

            text = QuestionQuality.clean(q.text or "")

            if "Ans." in text or "Solution" in text:
                print("=" * 80)
                print(f"BEFORE VALIDATOR {qid}")
                print(repr(text[:400]))
                print()

            text = re.sub(r"OCR\([^)]*\)", "", text)
            text = re.sub(r"\bQ\.\s*$", "", text, flags=re.M)

            # ---- FIXED: remove ONLY explicit page headers ----
            text = re.sub(
                r"(?im)^\s*(?:page|d\s*age)\s+\d+\s*.*$",
                "",
                text,
            )

            text = re.sub(r"\n{2,}", "\n", text)
            text = re.sub(r"[ \t]+", " ", text)
            text = text.strip()

            if "Ans." in text or "Solution" in text:
                print("=" * 80)
                print(f"AFTER VALIDATOR {qid}")
                print(repr(text[:400]))
                print("=" * 80)
                print()

            tokens = text.split()
            if tokens:
                short = sum(1 for t in tokens if len(t) == 1 and t.isalpha())
                if short / len(tokens) > 0.15:
                    print("=" * 80)
                    print(f"VALIDATOR DROP {qid}: too_many_single_letters")
                    print(repr(q.text[:300]))
                    print("=" * 80)
                    continue

            alpha = sum(c.isalpha() for c in text)

            print("=" * 80)
            print(f"ALPHA DEBUG {qid}")
            print("text:", repr(text[:200]))
            print("alpha:", alpha)
            print("=" * 80)

            if alpha < 10:
                print("=" * 80)
                print(f"VALIDATOR DROP {qid}: too_few_alpha (<10)")
                print("TEXT BEFORE ALPHA CHECK")
                print(repr(text))
                print("ALPHA COUNT =", alpha)
                print(repr(q.text[:300]))
                print("=" * 80)
                continue

            if len(tokens) < 4:
                print("=" * 80)
                print(f"VALIDATOR DROP {qid}: too_few_words (<4)")
                print(repr(q.text[:300]))
                print("=" * 80)
                continue

            completeness = CompletenessScorer.score(text)
            q.confidence = q.confidence * completeness

            if q.confidence < 0.45:
                print("=" * 80)
                print(f"VALIDATOR DROP {qid}: low_confidence (<0.45)")
                print(repr(q.text[:300]))
                print("=" * 80)
                continue

            if not QuestionSanity.valid(text):
                print("=" * 80)
                print(f"VALIDATOR DROP {qid}: sanity_check_failed")
                print(repr(q.text[:300]))
                print("=" * 80)
                continue

            q.text = text
            valid.append(q)

        return valid
