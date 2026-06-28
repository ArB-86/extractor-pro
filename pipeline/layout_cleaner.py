import re


class LayoutCleaner:

    _DATE = re.compile(r"^\d{2}/\d{2}/\d{2}$")
    _PAGE_NUM = re.compile(r"^\d{1,3}$")
    _YEAR_LINE = re.compile(r"^20\d{2}-\d{2}$")
    _STAMP_DATE = re.compile(r"^\d{2}-\d{2}-\d{4}$")

    _HEADER_MARKERS = (
        "EXEMPLAR PROBLEMS",
        "MATHEMATICS",
        "GANITA PRAKASH",
        "PAIR OF LINEAR EQUATIONS IN TWO VARIABLES",
        "THINK AND DISCUSS",
        "REVISE",
    )

    def __init__(self, blocks):
        self.blocks = blocks

    def process(self):

        cleaned = []

        for block in self.blocks:

            text = block.text.strip()

            if not text:
                continue

            if self._DATE.fullmatch(text):
                continue

            if self._PAGE_NUM.fullmatch(text):
                continue

            if self._YEAR_LINE.fullmatch(text):
                continue

            if self._STAMP_DATE.fullmatch(text):
                continue

            upper = text.upper()

            if any(marker in upper for marker in self._HEADER_MARKERS):
                if len(text.split()) <= 6:
                    continue

            if upper in {"INTEGERS", "SETS", "REAL NUMBERS"}:
                continue

            if re.fullmatch(r"[A-Z][A-Z\s]{5,50}\s+\d{1,3}", upper):
                continue

            cleaned.append(block)

        return cleaned
