from src.document.document import Document
from src.question.models import (
    QuestionCandidate,
    QuestionContext,
)
from src.question.patterns import (
    CHAPTER_PATTERN,
    EXERCISE_PATTERN,
    QUESTION_PATTERN,
    SUBQUESTION_PATTERN,
)


class QuestionSegmenter:

    def segment(
        self,
        document: Document,
    ) -> list[QuestionCandidate]:

        candidates = []

        context = QuestionContext()

        current = None

        for region in document.regions:

            if not region.text:
                continue

            text = region.text.strip()

            m = CHAPTER_PATTERN.match(text)

            if m:
                context.chapter = m.group(2).strip()
                continue

            m = EXERCISE_PATTERN.match(text)

            if m:
                context.exercise = m.group(1)
                continue

            m = QUESTION_PATTERN.match(text)

            if m:

                if current:
                    candidates.append(current)

                current = QuestionCandidate(
                    number=m.group(1),
                    text=m.group(2).strip(),
                    context=QuestionContext(
                        chapter=context.chapter,
                        exercise=context.exercise,
                        page=region.page,
                    ),
                )

                continue

            m = SUBQUESTION_PATTERN.match(text)

            if m and current:

                current.text += "\n" + text

                continue

            if current:

                current.text += "\n" + text

        if current:

            candidates.append(current)

        return candidates
