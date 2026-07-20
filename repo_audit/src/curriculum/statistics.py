from collections import Counter


class CurriculumStatistics:

    def build(self, manifests):

        return {
            "total": len(manifests),
            "by_class": dict(
                Counter(
                    m.get("class")
                    for m in manifests
                )
            ),
            "by_book_type": dict(
                Counter(
                    m.get("book_type")
                    for m in manifests
                )
            ),
        }
