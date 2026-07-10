from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class ExtractionResult:

    questions: list

    manifest: dict

    statistics: dict

    search_index: dict

    output_directory: str

    evaluation: dict[str, Any] | None = None
