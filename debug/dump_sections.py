from parsers.pdf_parser import PDFParser
from pipeline.section_parser import SectionParser

PDF = "/home/jiitcah.05/nlp_research_module/datasets/exemplar_raw/10th_maths/jeep203.pdf"

blocks = PDFParser(PDF).extract()

sections = SectionParser(blocks).parse()

print("Sections:", len(sections))

for s in sections:

    print("=" * 80)
    print(s.title)
    print("Pages:", s.page_start, "-", s.page_end)
    print("Blocks:", len(s.blocks))

    if s.blocks:
        print("\nFirst Block:\n")
        print(s.blocks[0].text[:400])

        print("\nLast Block:\n")
        print(s.blocks[-1].text[:400])
