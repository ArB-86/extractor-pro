VALID_LABELS = {
    "title",
    "plain text",
    "isolate formula",
    "table",
    "table caption",
}


class LayoutFilter:

    def filter(self, boxes):
        filtered = []

        for box in boxes:
            # Normalize label: replace underscores with spaces, strip, lower
            label = box.label.replace("_", " ").strip().lower()

            if label not in VALID_LABELS:
                continue

            if box.confidence < 0.50:
                continue

            filtered.append(box)

        return filtered
