from src.dataset.builder import DatasetBuilder


class DatasetPipeline:

    def __init__(self):

        self.builder = DatasetBuilder()

    def run(self, questions):

        self.builder.extend(questions)

        return self.builder.build()
