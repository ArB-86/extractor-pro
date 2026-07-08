from src.document.document import Document
from src.document.question import Question


class QuestionExtractor:

    def extract(self, document: Document) -> list[Question]:

        questions = []

        for region in document.regions:

            if not region.text:
                continue

            text = region.text.strip()

            if len(text) < 15:
                continue

            questions.append(
                Question(
                    question_text=text,
                    chapter=None,
                    confidence=region.confidence,
                )
            )

        return questions
