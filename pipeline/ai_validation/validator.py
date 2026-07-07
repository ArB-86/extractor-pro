from pipeline.ai_validation.schema import ValidationResult


class AIValidator:

    def __init__(self,model):
        self.model=model

    def validate(self,pdf_page,question):

        return self.model.validate(
            pdf_page=pdf_page,
            question=question,
        )
