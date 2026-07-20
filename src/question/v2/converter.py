from __future__ import annotations

import hashlib
import re

from rapidfuzz import fuzz

from src.document.question import Question
from src.question.models import QuestionCandidate


class CandidateConverter:

    SIMILARITY = 98.0

    @staticmethod
    def _normalize(text: str) -> str:

        text = text.lower()
        text = re.sub(r"\s+", " ", text)
        text = re.sub(r"[^\w ]", "", text)

        return text.strip()

    @staticmethod
    def _fingerprint(text: str) -> str:

        text = CandidateConverter._normalize(text)

        text = re.sub(r"\d+", "", text)
        text = re.sub(r"\s+", " ", text)

        return hashlib.sha1(
            text.encode("utf-8")
        ).hexdigest()

    def convert(
        self,
        candidates: list[QuestionCandidate],
    ) -> list[Question]:

        output = []

        seen = {}

        for q in candidates:

            # ---- Split question_text and answer ----
            question_text = q.text
            answer = None

            m = re.search(
                r"\b(?:Ans(?:wer)?|Solution)\s*[:.]?\s*",
                q.text,
                flags=re.IGNORECASE,
            )

            if m:
                question_text = q.text[:m.start()].strip()
                answer = q.text[m.end():].strip()

                # ---- DEBUG ----
                print("=" * 80)
                print("ANSWER SPLIT")
                print("MATCH:", m.group(0))
                print("QUESTION:", question_text[:120])
                print("ANSWER:", answer[:120] if answer else None)
                print("=" * 80)

            norm = self._normalize(question_text)
            fp = self._fingerprint(question_text)

            key = (
                q.context.chapter,
                q.context.section,
                q.context.exercise,
                q.number,
            )

            duplicate = False

            for prev_fp, prev_norm in seen.get(key, ()):

                if fp == prev_fp:
                    duplicate = True
                    break

                if fuzz.ratio(norm, prev_norm) >= self.SIMILARITY:
                    duplicate = True
                    break

            if duplicate:
                continue

            seen.setdefault(key, []).append(
                (fp, norm)
            )

            output.append(

                Question(

                    question_text=question_text,

                    answer=answer,

                    chapter=q.context.chapter,

                    exercise=q.context.exercise,

                    question_number=q.number,

                    source_page=q.context.page,

                    source_type=q.context.source_type,

                    question_type=q.qtype.value,

                    confidence=q.confidence,

                    metadata={

                        **q.metadata,

                        "chapter": q.context.chapter,
                        "exercise": q.context.exercise,
                        "section": q.context.section,
                        "page": q.context.page,
                        "source_type": q.context.source_type,

                    },

                )

            )

        # ---- DEBUG: Simplified warning ----
        print("=" * 80)
        print("CONVERTER SUMMARY")
        print("=" * 80)
        print("Input :", len(candidates))
        print("Output:", len(output))

        if len(output) != len(candidates):
            print("=" * 80)
            print("CONVERTER WARNING")
            print(f"Input : {len(candidates)}")
            print(f"Output: {len(output)}")
            print("=" * 80)

        print("=" * 80)
        print("RETURNING FROM CONVERTER")
        print("len(output) =", len(output))
        print("=" * 80)

        return output
