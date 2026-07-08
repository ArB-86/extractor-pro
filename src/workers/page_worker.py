from pathlib import Path

from src.pipeline.layout_pipeline import LayoutPipeline
from src.document.builder import DocumentBuilder
from src.markdown.builder import MarkdownBuilder
from src.llm.qwen_client import QwenClient


def process_page(job):
    image_path, output_dir, page_no = job

    page_dir = Path(output_dir)
    page_dir.mkdir(parents=True, exist_ok=True)

    regions = LayoutPipeline().run(
        image_path,
        str(page_dir),
        page=page_no,
    )

    doc = DocumentBuilder.build(regions)

    md_path = page_dir / "page.md"
    MarkdownBuilder.save(doc, md_path)

    clean = QwenClient().chat(
        md_path.read_text(encoding="utf-8")
    )

    (page_dir / "page_clean.md").write_text(
        clean,
        encoding="utf-8",
    )

    return page_no
