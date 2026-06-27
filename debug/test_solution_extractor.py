from pipeline.extractors.solution_extractor import SolutionExtractor

clf = SolutionExtractor()

tests = [

"""
Question...

Solution :
The answer is x=5.
""",

"""
Find x.
""",

"""
Solution:
First solve the equation.
Then simplify.
Finally x=7.
"""
]

for t in tests:

    print("=" * 40)

    print(clf.extract(t))
