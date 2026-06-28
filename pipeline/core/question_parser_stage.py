from pipeline.core.stage import Stage
from pipeline.question_parser import QuestionParser


class QuestionParserStage(Stage):

    def run(self, context):

        if context.metadata.get("skip"):
            return context

        questions = []
        source = context.metadata.get("source", "NCERT")
        chapter = context.metadata.get("chapter", "")

        for section in context.metadata["sections"]:

            questions.extend(
                QuestionParser(
                    section,
                    source=source,
                    chapter=chapter,
                ).parse()
            )

        context.questions = self._deduplicate(questions)

        return context

    def _deduplicate(self, questions):

        seen: set[tuple[str, int, str]] = set()
        unique = []

        for q in questions:

            key = (q.exercise, q.id, " ".join(q.question.split()).lower())

            if key in seen:
                continue

            seen.add(key)
            unique.append(q)

        return unique
