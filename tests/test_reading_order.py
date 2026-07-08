from src.pipeline.layout_pipeline import LayoutPipeline

pipeline = LayoutPipeline()

regions = pipeline.run(
    "data/rendered/fegp101/page_001.png",
    "debug/pipeline",
)

print("\nReading Order\n")
print("=" * 80)

for i, r in enumerate(regions):
    print(
        f"{i:02d}",
        r.label,
        f"y={r.y1:.1f}",
        f"x={r.x1:.1f}",
    )
