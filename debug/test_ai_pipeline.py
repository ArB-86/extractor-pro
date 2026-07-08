
from pipeline.ai.model import DummyModel
from pipeline.ai.pipeline import AIPipeline

pipe = AIPipeline(DummyModel())

print(pipe.ocr.repair("12. Pr0ve thaf sin²x+cos²x=1"))
print()

print(pipe.formula.repair("sin2x+co52x"))
print()

print(pipe.figure.analyze("Find angle A"))
