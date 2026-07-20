from src.document.builder import DocumentBuilder
from src.markdown.builder import MarkdownBuilder
from src.pipeline.layout_pipeline import LayoutPipeline

pipeline = LayoutPipeline()

regions = pipeline.run(
    "data/rendered/fegp101/page_001.png",
    "debug/pipeline",
)

doc = DocumentBuilder.build(regions)

output = MarkdownBuilder.save(
    doc,
    "debug/page.md",
)

print("=" * 80)
print(f"Saved markdown to: {output}")
print("=" * 80)