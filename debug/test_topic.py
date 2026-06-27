from types import SimpleNamespace

from pipeline.classifiers.topic import TopicClassifier

clf = TopicClassifier()

samples = [

    "Find the zeroes of the polynomial.",

    "Find the probability of drawing a king.",

    "Draw the graph of linear equations.",

    "Find the area of a sector of a circle.",

    "Evaluate sin45 + cos45."
]

for s in samples:

    q = SimpleNamespace(question=s)

    print(clf.classify(q), "->", s)
