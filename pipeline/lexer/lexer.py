from __future__ import annotations

from pipeline.models import Paragraph

from .tokens import Token


class Lexer:

    def tokenize(self, block: Paragraph) -> list[Token]:
        return []
