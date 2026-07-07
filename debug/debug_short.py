from parsers.pdf_parser import PDFParser

pdf = "/home/jiitcah.05/nlp_research_module/datasets/exemplar_raw/10th_maths/jeep208.pdf"

blocks = PDFParser(pdf).extract()

targets = [
    "12. Prove that",
    "13. Show that",
]

for target in targets:
    print("=" * 100)
    print(target)

    for i, b in enumerate(blocks):
        if target in b.text:
            print("=" * 100)
            for j in range(i - 5, i + 8):
                if j < 0 or j >= len(blocks):
                    continue
                print(f"\nBLOCK {j}")
                print(repr(blocks[j].text))
                print("PAGE:", blocks[j].page)
                print("BBOX:", blocks[j].bbox)
            break
