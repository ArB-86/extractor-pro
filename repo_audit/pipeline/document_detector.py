class DocumentDetector:

    def detect(self, blocks):

        # Look much deeper into the document
        text = "\n".join(
            b.text.upper()
            for b in blocks[:250]
        )

        # Highest priority
        if "EXERCISE" in text:
            return "EXEMPLAR"

        # Sample paper
        if (
            "SECTION A" in text
            and "GENERAL INSTRUCTIONS" in text
        ):
            return "SAMPLE_PAPER"

        # Textbook
        if (
            "CHAPTER" in text
            and "MAIN CONCEPTS AND RESULTS" not in text
        ):
            return "TEXTBOOK"

        return "UNKNOWN"