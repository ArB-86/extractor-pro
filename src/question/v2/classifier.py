import re

from __future__ import annotations

from src.question.models import (
    QuestionCandidate,
    QuestionType,
)


class QuestionClassifier:

    def classify(
        self,
        questions: list[QuestionCandidate],
    ) -> list[QuestionCandidate]:

        option_pattern = re.compile(
            r"\([a-d]\)|^[a-d][.)]",
            re.IGNORECASE | re.MULTILINE,
        )

        for q in questions:

            text = q.text.lower()

            option_count = len(
                option_pattern.findall(text)
            )

            if (
                "choose the correct" in text
                or option_count >= 2
            ):
                q.qtype = QuestionType.MCQ

            elif "fill in the blank" in text or "____" in text:
                q.qtype = QuestionType.FILL

            elif "true or false" in text:
                q.qtype = QuestionType.TRUE_FALSE

            elif "assertion" in text and "reason" in text:
                q.qtype = QuestionType.ASSERTION_REASON

            elif "case study" in text:
                q.qtype = QuestionType.CASE_STUDY

            elif "construct" in text:
                q.qtype = QuestionType.CONSTRUCTION

            elif "prove" in text:
                q.qtype = QuestionType.PROOF

            elif "activity" in text:
                q.qtype = QuestionType.ACTIVITY

            elif option_count >= 4:

                q.qtype = QuestionType.MCQ

            elif len(text.split()) > 70:
                q.qtype = QuestionType.LONG

            else:
                q.qtype = QuestionType.SHORT

        return questions
