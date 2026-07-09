
from __future__ import annotations

from src.document.question import Question
from src.question.models import QuestionCandidate


class CandidateConverter:

    def convert(
        self,
        candidates: list[QuestionCandidate],
    ) -> list[Question]:

        output = []

        for q in candidates:

            output.append(

                Question(

                    question_text=q.text,

                    chapter=q.context.chapter,

                    exercise=q.context.exercise,

                    question_number=q.number,

                    question_type=q.qtype.value,

                    confidence=q.confidence,

                    metadata=q.metadata,

                )

            )

        return output
