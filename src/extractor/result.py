
from dataclasses import dataclass


@dataclass(slots=True)
class ExtractionResult:

    questions: list

    manifest: dict

    statistics: dict

    search_index: dict

    output_directory: str
