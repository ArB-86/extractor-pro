from collections import defaultdict


class CurriculumCatalog:

    def build(self, manifests):

        catalog = defaultdict(lambda: defaultdict(list))

        for m in manifests:

            cls = m.get("class")
            book = m.get("book_type")

            if cls is None or book is None:
                continue

            catalog[cls][book].append(
                {
                    "chapter": m.get("chapter"),
                    "file": m.get("file"),
                    "sha256": m.get("sha256"),
                }
            )

        return {
            cls: dict(books)
            for cls, books in catalog.items()
        }
