from pipeline.question_parser_v2.question_splitter import QuestionSplitter

text = (
    "2. Is 3 ! + 4 ! = 7 ! ? "
    "3. Compute "
    "4. If , find x"
)

for q in QuestionSplitter().split(text):
    print("-" * 60)
    print(q)
