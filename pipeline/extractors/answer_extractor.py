import re


class AnswerExtractor:

    ANSWER_PATTERNS = [
        re.compile(r"Answer\s*[:\-]\s*(.+)", re.I),
        re.compile(r"Ans\.?\s*[:\-]\s*(.+)", re.I),
        re.compile(r"Correct\s*Answer\s*[:\-]\s*(.+)", re.I),
    ]

    def extract(self, text: str):

        if not text:
            return None

        for pattern in self.ANSWER_PATTERNS:

            m = pattern.search(text)

            if m:
                return m.group(1).strip()

        return None
