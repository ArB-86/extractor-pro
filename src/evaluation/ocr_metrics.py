from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class OCRMetrics:
    character_errors: int = 0
    character_total: int = 0
    word_errors: int = 0
    word_total: int = 0

    @property
    def cer(self) -> float:
        return 0.0 if self.character_total == 0 else self.character_errors / self.character_total

    @property
    def wer(self) -> float:
        return 0.0 if self.word_total == 0 else self.word_errors / self.word_total

    def to_dict(self) -> dict:
        return {
            "character_errors": self.character_errors,
            "character_total": self.character_total,
            "word_errors": self.word_errors,
            "word_total": self.word_total,
            "cer": round(self.cer, 6),
            "wer": round(self.wer, 6),
        }
