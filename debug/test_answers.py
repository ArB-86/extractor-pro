from pipeline.answer_parser import AnswerParser

samples = [
    "Solution : Answer (C)",
    "Answer (B)",
    "Answer: D",
    "Solution : Answer(A)"
]

parser = AnswerParser()

for s in samples:
    print(s, "->", parser.parse(s))
