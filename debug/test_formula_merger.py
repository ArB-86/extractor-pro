from pipeline.math.formula_merger import FormulaMerger

m = FormulaMerger()

tests = [

"cos\nθ",

"sin\nA",

"x\n2",

"tan\nθ + sec\nθ",

"cos\nθ\nθ"

]

for t in tests:

    print("=" * 40)

    print(m.merge(t))
