from pathlib import Path

from src.document.document import Document


class MarkdownBuilder:

    @staticmethod
    def build(doc: Document) -> str:
        """
        Convert a Document into Markdown.
        """

        md = []

        for region in doc.regions:

            if not region.text:
                continue

            text = region.text.strip()

            if region.label == "title":
                md.append(f"# {text}")

            elif region.label == "plain_text":
                md.append(text)

            elif region.label == "table_caption":
                md.append(f"**{text}**")

            elif region.label == "figure_caption":
                md.append(f"*{text}*")

            else:
                md.append(text)

        return "\n\n".join(md)

    @staticmethod
    def save(doc: Document, output_path: str):
        """
        Save the generated markdown to disk.
        """

        markdown = MarkdownBuilder.build(doc)

        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        output_path.write_text(
            markdown,
            encoding="utf-8",
        )

        return output_path