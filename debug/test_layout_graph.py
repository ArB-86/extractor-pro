from parsers.pdf_parser import PDFParser
from pipeline.layout.layout_graph import LayoutGraph

pdf = "/home/jiitcah.05/nlp_research_module/datasets/exemplar_raw/10th_maths/jeep208.pdf"

blocks = PDFParser(pdf).extract()

graph = LayoutGraph().build(blocks)

print("Pages:", len(graph))

for page in sorted(graph)[:3]:

    print("=" * 80)
    print("PAGE", page)

    for node in graph[page][:5]:

        print(node["bbox"])
        print(node["text"][:80])
        print()
