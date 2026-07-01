import sys
from pathlib import Path
import json
sys.path.insert(0, '.')

from pipeline.question_parser import QuestionParser
from parsers.pdf_parser import PDFParser

print("Using improved QuestionParser")

pdf_path = sys.argv[1]
pdf_name = Path(pdf_path).stem

blocks = PDFParser(pdf_path).extract()
qs = QuestionParser(blocks).parse()

output_dir = Path("output/json")
output_dir.mkdir(parents=True, exist_ok=True)
output_file = output_dir / f"{pdf_name}.json"

output = [{"id": q.id, "question": q.question, "chapter": "all", "source_pdf": pdf_name} for q in qs]

with open(output_file, "w") as f:
    json.dump(output, f, indent=2)

print(f"Real extraction: {len(qs)} questions from {pdf_name}. Saved.")
