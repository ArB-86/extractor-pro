from parsers.pdf_parser import PDFParser
from pipeline.paragraph_builder import ParagraphBuilder
from pipeline.question_parser import QuestionParser

PDF = "/home/jiitcah.05/nlp_research_module/datasets/exemplar_raw/10th_maths/jeep203.pdf"

blocks = PDFParser(PDF).extract()
paragraphs = ParagraphBuilder(blocks).build()
questions = QuestionParser(paragraphs).parse()

with open("questions_dump.txt", "w", encoding="utf8") as f:

    for q in questions:

        f.write("=" * 100 + "\n")
        f.write(f"QUESTION {q.id}\n")
        f.write(f"PAGE : {q.page_start}-{q.page_end}\n\n")
        f.write(q.question)
        f.write("\n\n")

print("Saved", len(questions), "questions")
