from pathlib import Path

from parsers.pdf_parser import PDFParser
from pipeline.layout.line_extractor import LineExtractor
from pipeline.question_parser_v2.exercise_tracker import ExerciseTracker
from pipeline.question_parser_v2.question_builder import QuestionBuilder

pdf = Path(
    "/home/jiitcah.05/nlp_research_module/datasets/raw_docs/kemh1dd/kemh106.pdf"
)

blocks = PDFParser(str(pdf)).extract()
lines = LineExtractor().extract(blocks)

tracker = ExerciseTracker()

builder = QuestionBuilder()

questions = builder.build(lines, tracker)

print("=" * 80)
print("Questions:", len(questions))
print("=" * 80)

for q in questions[:10]:

    print()
    print("=" * 80)
    print(q.id)
    print(q.exercise)
    print(q.chapter)
    print("-" * 80)
    print(q.question[:500])
