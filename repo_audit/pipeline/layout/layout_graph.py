from __future__ import annotations


class LayoutGraph:

    def build(self, blocks):

        pages = {}

        for block in blocks:

            page = block.page

            pages.setdefault(page, [])

            pages[page].append(
                {
                    "text": block.text,
                    "bbox": block.bbox,
                    "page": page,
                }
            )

        for page in pages:
            pages[page].sort(
                key=lambda x: (
                    x["bbox"][1],
                    x["bbox"][0],
                )
            )

        return pages
