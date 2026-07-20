from __future__ import annotations

import re
from rapidfuzz import fuzz

from src.document.question import Question


class TeacherGuideFilter:

    SIMILARITY = 99.5  # only near‑identical texts

    @staticmethod
    def normalize(text: str) -> str:
        text = text.lower()
        text = re.sub(r"\s+", " ", text)
        return text.strip()

    def process(
        self,
        questions: list[Question],
    ) -> list[Question]:

        output = []

        for q in questions:

            duplicate = False
            norm = self.normalize(q.question_text)

            for prev in output:

                # ---- Context key: only compare same chapter, page, question number ----
                if (
                    prev.chapter != q.chapter
                    or prev.source_page != q.source_page
                    or prev.question_number != q.question_number
                ):
                    continue

                score = fuzz.ratio(
                    norm,
                    self.normalize(prev.question_text),
                )

                if score < self.SIMILARITY:
                    continue

                # Prefer textbook over guide/recap
                if (
                    prev.source_type == "textbook"
                    and q.source_type != "textbook"
                ):
                    duplicate = True
                    print("=" * 80)
                    print("TEACHER FILTER DROP (recap)")
                    print("DROPPED:", q.question_number, q.source_type)
                    print("KEPT:", prev.question_number, prev.source_type)
                    print("CHAPTER:", q.chapter)
                    print("PAGE:", q.source_page)
                    print("TEXT:", repr(q.question_text[:300]))
                    print("=" * 80)
                    break

                if (
                    q.source_type == "textbook"
                    and prev.source_type != "textbook"
                ):
                    output.remove(prev)
                    print("=" * 80)
                    print("TEACHER FILTER REPLACE (textbook wins)")
                    print("DROPPED:", prev.question_number, prev.source_type)
                    print("KEPT:", q.question_number, q.source_type)
                    print("CHAPTER:", q.chapter)
                    print("PAGE:", q.source_page)
                    print("TEXT:", repr(q.question_text[:300]))
                    print("=" * 80)
                    break

                duplicate = True
                print("=" * 80)
                print("TEACHER FILTER DUPLICATE (same context)")
                print("Question:", q.question_number, q.source_type)
                print("Chapter:", q.chapter)
                print("PAGE:", q.source_page)
                print("TEXT:", repr(q.question_text[:300]))
                print("=" * 80)
                break

            if not duplicate:
                output.append(q)

        return output
