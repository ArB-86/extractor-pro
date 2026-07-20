from __future__ import annotations

import re


class OCRPostProcessor:
    """
    Cleans raw OCR output before it enters the document pipeline.
    This module should never remove mathematical meaning.
    """

    _spaces = re.compile(r"[ \t]+")
    _blank = re.compile(r"\n{3,}")

    # isolated OCR garbage:
    # " t "
    # " g "
    # " r "
    # but keep x y z n if mathematical.
    _isolated = re.compile(
        r"(?<![A-Za-z0-9])([bcdfghjklmprstvwx])(?![A-Za-z0-9])",
        re.I,
    )

    COMMON = {
        "thatis": "That is",
        "doyou": "do you",
        "canyou": "can you",
        "whatis": "what is",
        "whydoes": "why does",
    }

    @classmethod
    def clean(cls, text: str) -> str:

        if not text:
            return ""

        text = text.replace("\r", "")

        # normalize spaces
        text = cls._spaces.sub(" ", text)

        # remove OCR junk letters
        text = cls._isolated.sub("", text)

        # remove spaces before punctuation
        text = re.sub(
            r"\s+([,.;:!?])",
            r"\1",
            text,
        )

        # normalize blank lines
        text = cls._blank.sub("\n\n", text)

        # join broken words across lines
        text = re.sub(
            r"([a-z])\n([a-z])",
            r"\1 \2",
            text,
            flags=re.I,
        )

        # fix duplicated punctuation
        text = re.sub(r"\.{2,}", "...", text)
        text = re.sub(r",{2,}", ",", text)
        text = re.sub(r"\?{2,}", "?", text)

        # apply common phrase repairs
        for bad, good in cls.COMMON.items():
            text = re.sub(
                bad,
                good,
                text,
                flags=re.I,
            )

        return text.strip()
