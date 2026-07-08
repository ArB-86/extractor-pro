from src.validator.question_validator import QuestionValidator


class ValidationPipeline:

    def __init__(self):

        self.validator = QuestionValidator()

    def run(self, questions):

        return self.validator.validate_many(
            questions
        )
