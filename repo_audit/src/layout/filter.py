VALID_LABELS = {
    "title",
    "plain text",
    "isolate_formula",
    "table",
    "table_caption",
}


class LayoutFilter:

    def filter(self, boxes):

        filtered = []

        for box in boxes:

            if box.label not in VALID_LABELS:
                continue

            if box.confidence < 0.50:
                continue

            filtered.append(box)

        return filtered
