from __future__ import annotations

import re


def normalize_pua(text: str) -> str:
    """Decode NCERT PDF private-use-area font encoding (U+F000–U+F0FF)."""
    if not text:
        return text

    out: list[str] = []
    for char in text:
        code = ord(char)
        if 0xF000 <= code <= 0xF0FF:
            out.append(chr(code - 0xF000))
        else:
            out.append(char)
    return "".join(out)


def normalize_text(text: str) -> str:
    text = normalize_pua(text)
    text = text.replace("\u00ad", "")  # soft hyphen
    text = re.sub(r"[ \t]+\n", "\n", text)
    return text.strip()
