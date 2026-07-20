from __future__ import annotations

import re


class TextRepair:

    SINGLE_LETTER = re.compile(
        r"(?<=\s)[a-zA-Z](?=\s)",
    )

    MULTISPACE = re.compile(r"[ \t]{2,}")

    @classmethod
    def repair(cls, text: str) -> str:

        if not text:
            return ""

        text = text.replace("\r", "")

        # Remove isolated OCR letters
        text = cls.SINGLE_LETTER.sub("", text)

        # Join broken words
        text = re.sub(
            r"([a-z])\n([a-z])",
            r"\1 \2",
            text,
            flags=re.I,
        )

        # Collapse spaces
        text = cls.MULTISPACE.sub(" ", text)

        # Remove spaces before punctuation
        text = re.sub(r"\s+([.,;:!?])", r"\1", text)

        # Collapse blank lines
        text = re.sub(r"\n{2,}", "\n", text)

        return text.strip()
