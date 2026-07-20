import fitz

from pipeline.models import SemanticBlock, BlockType


FLAGS = (
    fitz.TEXT_PRESERVE_WHITESPACE
    | fitz.TEXT_PRESERVE_LIGATURES
)


class PDFParser:

    def __init__(self, pdf_path):
        self.pdf_path = pdf_path

    def extract(self):

        doc = fitz.open(self.pdf_path)

        blocks = []

        for page_no, page in enumerate(doc, start=1):

            page_dict = page.get_text(
                "dict",
                flags=FLAGS,
            )

            width = page.rect.width
            height = page.rect.height

            for block in page_dict.get("blocks", []):

                if block.get("type") != 0:
                    continue

                lines = block.get("lines", [])

                if not lines:
                    continue

                spans = []

                for line in lines:
                    spans.extend(line.get("spans", []))

                text = "\n".join(
                    "".join(
                        span.get("text", "")
                        for span in line.get("spans", [])
                    )
                    for line in lines
                ).strip()

                if not text:
                    continue

                fonts = [
                    s.get("font", "")
                    for s in spans
                ]

                sizes = [
                    round(s.get("size", 0), 2)
                    for s in spans
                ]

                flags = [
                    s.get("flags", 0)
                    for s in spans
                ]

                blocks.append(

                    SemanticBlock(

                        page=page_no,

                        text=text,

                        bbox=tuple(block["bbox"]),

                        raw_lines=lines,

                        block_type=BlockType.PARAGRAPH,

                        metadata={

                            "page_width": width,

                            "page_height": height,

                            "font": max(
                                set(fonts),
                                key=fonts.count
                            ) if fonts else "",

                            "font_size": max(
                                set(sizes),
                                key=sizes.count
                            ) if sizes else 0,

                            "font_flags": max(
                                set(flags),
                                key=flags.count
                            ) if flags else 0,

                            "line_count": len(lines),

                            "span_count": len(spans)

                        }

                    )

                )

        doc.close()

        return blocks

