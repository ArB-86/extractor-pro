from __future__ import annotations

from src.question.v2.extractor import QuestionExtractorV2


class QuestionPipeline:

    def __init__(self):
        self.extractor = QuestionExtractorV2()

    def run(self, document):
        return self.extractor.extract(document)
