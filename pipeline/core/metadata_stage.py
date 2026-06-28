from pathlib import Path

from pipeline.core.stage import Stage
from pipeline.metadata import (
    chapter_from_stem,
    class_from_pdf_path,
    document_kind,
    is_sample_paper_text,
    should_skip_pdf,
    source_label,
)


class MetadataStage(Stage):

    def run(self, context):

        pdf_path = context.pdf

        if should_skip_pdf(pdf_path):
            context.metadata["skip"] = True
            context.metadata["skip_reason"] = "appendix_or_supplement"
            return context

        kind = document_kind(pdf_path)
        stem = chapter_from_stem(Path(pdf_path).stem)

        context.metadata.update(
            {
                "kind": kind,
                "chapter": stem,
                "class": class_from_pdf_path(pdf_path),
                "source": source_label(kind),
                "skip": False,
            }
        )

        return context


class DocumentGateStage(Stage):

    def run(self, context):

        if context.metadata.get("skip"):
            return context

        sample_text = "\n".join(
            block.text
            for block in context.blocks[:40]
        )

        if is_sample_paper_text(sample_text):
            context.metadata["skip"] = True
            context.metadata["skip_reason"] = "sample_paper"

        return context
