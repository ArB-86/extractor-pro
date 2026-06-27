from types import SimpleNamespace

from pipeline.classifiers.difficulty import DifficultyClassifier

samples = [
    "Find the value of x.",
    "Show that tan²A + 1 = sec²A.",
    "Construct a triangle ABC.",
    "Draw the graph of y=x.",
    "Prove that if sinθ+cosθ=p then..."
]

clf = DifficultyClassifier()

for s in samples:

    q = SimpleNamespace(
        question=s,
        options={}
    )

    print(clf.classify(q), "->", s)