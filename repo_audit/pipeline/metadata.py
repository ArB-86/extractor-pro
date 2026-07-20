from __future__ import annotations

import re
from pathlib import Path

EXEMPLAR_PREFIX_CLASS: dict[str, int] = {
    "feep": 6,
    "gemp": 7,
    "heep": 8,
    "ieep": 9,
    "jeep": 10,
    "keep": 11,
}

TEXTBOOK_FOLDER_CLASS: dict[str, int] = {
    "fegp1dd": 6,
    "gegp1dd": 7,
    "gegp2dd": 7,
    "hegp1dd": 8,
    "hegp2dd": 8,
    "iemh1dd": 9,
    "jemh1dd": 10,
    "kemh1dd": 11,
}

SKIP_NAME_PARTS = ("ps", "an", "a1", "a2", "sm")


def chapter_from_stem(stem: str) -> str:
    return stem.lower()


def class_from_pdf_path(pdf_path: str | Path) -> int | None:
    path = Path(pdf_path)
    stem = path.stem.lower()

    for prefix, grade in EXEMPLAR_PREFIX_CLASS.items():
        if stem.startswith(prefix):
            return grade

    parent = path.parent.name.lower()
    if parent in TEXTBOOK_FOLDER_CLASS:
        return TEXTBOOK_FOLDER_CLASS[parent]

    return None


def document_kind(pdf_path: str | Path) -> str:
    path = Path(pdf_path)
    stem = path.stem.lower()

    for prefix in EXEMPLAR_PREFIX_CLASS:
        if stem.startswith(prefix):
            return "exemplar"

    parent = path.parent.name.lower()
    if parent in TEXTBOOK_FOLDER_CLASS:
        return "textbook"

    return "unknown"


def should_skip_pdf(pdf_path: str | Path) -> bool:
    path = Path(pdf_path)
    stem = path.stem.lower()

    for part in SKIP_NAME_PARTS:
        if stem.endswith(part):
            return True

    return False


def is_sample_paper_text(text: str) -> bool:
    upper = text.upper()
    return (
        "DESIGN OF THE QUESTION PAPER" in upper
        or "DESIGN  OF  THE  QUESTION  PAPER" in upper
    )


def source_label(kind: str) -> str:
    if kind == "exemplar":
        return "NCERT Exemplar"
    if kind == "textbook":
        return "NCERT Textbook"
    return "NCERT"
