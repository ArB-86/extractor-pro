import re


class TextCleaner:

    @staticmethod
    def clean(text: str) -> str:
        if not text:
            return ""

        # Normalize line endings
        text = text.replace("\r", "")

        # Remove extra spaces
        text = re.sub(r"[ \t]+", " ", text)

        # Fix words split by newline
        text = re.sub(r"([a-zA-Z])\n([a-zA-Z])", r"\1 \2", text)

        # Fix hyphenated words across lines
        text = re.sub(r"(\w)-\n(\w)", r"\1\2", text)

        # Collapse multiple blank lines
        text = re.sub(r"\n{3,}", "\n\n", text)

        return text.strip()
