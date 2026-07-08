from pipeline.ai.factory import create_model
from pipeline.ai_validation.validator import AIValidator

model=create_model()

validator=AIValidator(model)

print("AI validator ready")
