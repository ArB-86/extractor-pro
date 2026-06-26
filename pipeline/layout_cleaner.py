import re


class LayoutCleaner:

    def __init__(self, blocks):
        self.blocks = blocks

    def process(self):

        cleaned = []

        for block in self.blocks:

            text = block.text.strip()

            if not text:
                continue

            # remove dates like 03/05/18
            if re.fullmatch(r"\d{2}/\d{2}/\d{2}", text):
                continue

            # remove page number only
            if re.fullmatch(r"\d+", text):
                continue

            # remove repeated headers
            if "PAIR OF LINEAR EQUATIONS IN TWO VARIABLES" in text.upper():
                continue

            if "EXEMPLAR PROBLEMS" in text.upper():
                continue

            cleaned.append(block)

        return cleaned
