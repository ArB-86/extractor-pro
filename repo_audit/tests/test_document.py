from src.document.builder import DocumentBuilder
from src.pipeline.layout_pipeline import LayoutPipeline

pipeline = LayoutPipeline()

regions = pipeline.run(
    "data/rendered/fegp101/page_001.png",
    "debug/pipeline",
)

doc = DocumentBuilder.build(regions)

print("=" * 80)
print("Pages:", doc.pages)

print()

print("Titles:")
for t in doc.titles:
    print("-", t.text)

print()

print("Paragraphs:", len(doc.paragraphs))

print()

print("=" * 80)
print(doc.text[:1000])
