from pipeline.extractors.answer_extractor import AnswerExtractor

clf = AnswerExtractor()

tests = [
    "Answer: (B)",
    "Ans: 27 cm",
    "Correct Answer : Option C",
    "Find x.",
]

for t in tests:
    print(clf.extract(t))
