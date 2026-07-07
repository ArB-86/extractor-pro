from __future__ import annotations

from pipeline.models.question import Question
from pipeline.question_parser_v2.question_classifier import (
    QuestionClassifier,
    QUESTION,
    CONTINUATION,
    OPTION,
    HEADING,
    NOISE,
)


class QuestionBuilder:

    def __init__(self):

        self.classifier = QuestionClassifier()

    def build(
        self,
        lines,
        tracker,
    ):

        questions = []

        current = None

        qid = 1

        for line in lines:

            tracker.update(line)

            kind = self.classifier.classify(line)

            # -------------------------------
            # Heading => close current question
            # -------------------------------
            if kind == HEADING:

                if current is not None:

                    questions.append(current)

                    current = None

                continue

            # -------------------------------
            # Start of a new question
            # -------------------------------
            if kind == QUESTION:

                if current is not None:
                    questions.append(current)

                current = Question(
                    question_id=qid,
                    source="",
                    chapter=tracker.section,
                    page_start=line.page,
                    page_end=line.page,
                    exercise=tracker.exercise,
                    question_type="unknown",
                    question="",
                )

                qid += 1

                continue

            # -------------------------------
            # Ignore everything until a question starts
            # -------------------------------
            if current is None:
                continue

            # -------------------------------
            # Skip page headers / figure labels
            # -------------------------------
            if kind == NOISE:
                continue

            current.page_end = line.page

            text = line.text.strip()

            if not text:
                continue

            if current.question:
                current.question += "\n"

            current.question += text

        if current is not None:
            questions.append(current)

        return questions