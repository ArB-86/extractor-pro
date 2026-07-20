from dataclasses import dataclass


@dataclass
class ExtractionStats:

    total_regions: int = 0
    skipped_regions: int = 0

    candidates: int = 0
    validated: int = 0
    converted: int = 0

    duplicates: int = 0

    answer_blocks: int = 0
    summary_blocks: int = 0
    page_headers: int = 0
