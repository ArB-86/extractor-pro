from pathlib import Path

from parsers.pdf_parser import PDFParser
from pipeline.layout.line_extractor import LineExtractor
from pipeline.layout_graph.graph import LayoutGraph

pdf = Path(
    "/home/jiitcah.05/nlp_research_module/datasets/raw_docs/kemh1dd/kemh106.pdf"
)

blocks = PDFParser(str(pdf)).extract()

lines = LineExtractor().extract(blocks)

nodes = LayoutGraph().build(lines)

print()

print("Blocks :", len(blocks))
print("Lines  :", len(lines))
print("Nodes  :", len(nodes))

print()

for node in nodes[:50]:

    print(
        node.id,
        node.prev,
        node.next,
        node.text[:80],
    )
