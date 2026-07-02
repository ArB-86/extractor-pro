from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .tokens import TokenType


@dataclass(slots=True)
class Token:
    """
    Atomic lexical unit extracted from a PDF line.

    This is intentionally lightweight.
    Higher-level structures (Question, Section, Table, etc.)
    will be built from sequences of Tokens.
    """

    type: TokenType

    text: str

    page: int

    bbox: tuple[float, float, float, float]

    raw_line: dict[str, Any]

    metadata: dict[str, Any] = field(default_factory=dict)

    confidence: float = 1.0

    def __str__(self) -> str:
        return f"{self.type.name}: {self.text}"

    def __repr__(self) -> str:
        return (
            f"Token("
            f"type={self.type.name}, "
            f"page={self.page}, "
            f"text={self.text!r}"
            f")"
        )