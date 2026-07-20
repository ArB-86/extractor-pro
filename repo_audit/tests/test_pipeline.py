from src.pipeline.layout_pipeline import LayoutPipeline

pipeline = LayoutPipeline()

regions = pipeline.run(

    image_path="data/rendered/fegp101/page_001.png",

    output_dir="debug/pipeline"

)

print()

print("=" * 80)

print(f"Detected {len(regions)} Regions\n")

for region in regions:

    print(region)