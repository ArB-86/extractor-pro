from parsers.pdf_parser import PDFParser
from pipeline.classifiers.question_classifier import QuestionClassifier
from pipeline.models import BlockType
import sys

blocks = PDFParser(sys.argv[1]).extract()

QuestionClassifier().classify(blocks)

questions = [
    b for b in blocks
    if b.block_type == BlockType.QUESTION
]

print("=" * 80)
print("QUESTION CLASSIFIER REPORT")
print("=" * 80)

print(f"Questions detected : {len(questions)}")
print()

for i, q in enumerate(questions, start=1):

    print("-" * 80)
    print(f"Question #{i}")
    print(f"Page : {q.page}")
    print(f"BBox : {q.bbox}")
    print()
    print(q.text)
    print()
