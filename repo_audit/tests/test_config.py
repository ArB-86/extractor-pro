from src.config.config import Config

layout = Config.load("layout")

ocr = Config.load("ocr")

pipeline = Config.load("pipeline")

print(layout)

print()

print(ocr)

print()

print(pipeline)
