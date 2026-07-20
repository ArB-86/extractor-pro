from __future__ import annotations

import re


class QuestionQuality:

    GARBAGE = re.compile(
        r"(?:\b[a-zA-Z]\b\s*){4,}"
    )

    @classmethod
    def clean(cls, text: str) -> str:

        if not text:
            return ""

        # collapse spaces
        text = re.sub(r"[ \t]+", " ", text)

        # remove repeated blank lines
        text = re.sub(r"\n{2,}", "\n", text)

        # remove long isolated-letter sequences
        text = cls.GARBAGE.sub("", text)

        # remove spaces before punctuation
        text = re.sub(r"\s+([,.;:!?])", r"\1", text)

        return text.strip()
