from pathlib import Path

from parsers.pdf_parser import PDFParser
from pipeline.layout.line_extractor import LineExtractor
from pipeline.question_parser_v2.exercise_tracker import ExerciseTracker

pdf = Path(
    "/home/jiitcah.05/nlp_research_module/datasets/raw_docs/kemh1dd/kemh106.pdf"
)

blocks = PDFParser(str(pdf)).extract()
lines = LineExtractor().extract(blocks)

tracker = ExerciseTracker()

last = None

for line in lines:

    tracker.update(line)

    state = (tracker.section, tracker.exercise)

    if state != last:

        print(
            f"P{line.page:02d}",
            tracker.section,
            "|",
            tracker.exercise,
        )

        last = state
