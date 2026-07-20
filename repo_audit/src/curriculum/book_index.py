from collections import defaultdict


class BookIndex:

    def build(self, manifests):

        index = defaultdict(list)

        for m in manifests:

            key = (
                m.get("class"),
                m.get("book_type"),
            )

            index[key].append(m)

        return dict(index)
