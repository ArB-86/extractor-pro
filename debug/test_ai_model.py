
from pipeline.ai.model import DummyModel

model = DummyModel()

print(
    model.generate(
        "Repair this OCR"
    )
)
