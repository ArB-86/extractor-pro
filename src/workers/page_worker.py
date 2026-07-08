from pathlib import Path

from src.pipeline.layout_pipeline import LayoutPipeline
from src.document.builder import DocumentBuilder


def process_page(job):

    image_path, output_dir, page_no = job

    page_dir = Path(output_dir)

    page_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    regions = LayoutPipeline().run(
        image_path=image_path,
        output_dir=str(page_dir),
        page=page_no,
    )

    document = DocumentBuilder.build(regions)

    return document
