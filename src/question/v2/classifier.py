from __future__ import annotations

import re

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
            re.I | re.M,
        )

        for q in questions:

            text = q.text.lower()

            option_count = max(
                len(option_pattern.findall(text)),
                q.metadata.get("option_count", 0),
            )

            if (
                "choose the correct" in text
                or option_count >= 2
            ):
                q.qtype = QuestionType.MCQ

            elif (
                "fill in the blank" in text
                or "____" in text
            ):
                q.qtype = QuestionType.FILL_IN_BLANK

            elif "true or false" in text:
                q.qtype = QuestionType.TRUE_FALSE

            elif (
                "assertion" in text
                and "reason" in text
            ):
                q.qtype = QuestionType.ASSERTION_REASON

            elif "case study" in text:
                q.qtype = QuestionType.CASE_STUDY

            elif len(text.split()) > 70:
                q.qtype = QuestionType.LONG_ANSWER

            else:
                q.qtype = QuestionType.SHORT_ANSWER

            if q.confidence < 0.45:
                q.metadata["review"] = True

            elif q.confidence > 0.90:
                q.metadata["trusted"] = True

        return questions
