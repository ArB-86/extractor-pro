from dataclasses import dataclass


@dataclass(slots=True)
class Source:

    book: str

    page: int

    pdf_sha256: str

    file_path: str
