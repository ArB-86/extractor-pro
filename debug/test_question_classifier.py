from pathlib import Path

from parsers.pdf_parser import PDFParser
from pipeline.layout.line_extractor import LineExtractor
from pipeline.question_parser_v2.question_classifier import QuestionClassifier

pdf = Path(
    "/home/jiitcah.05/nlp_research_module/datasets/raw_docs/kemh1dd/kemh106.pdf"
)

blocks = PDFParser(str(pdf)).extract()
lines = LineExtractor().extract(blocks)

clf = QuestionClassifier()

for line in lines:

    kind = clf.classify(line)

    if kind != "continuation":
        print(
            f"{line.page:02d}",
            f"{kind:12}",
            line.text,
        )
