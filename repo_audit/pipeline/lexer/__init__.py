"""
Extractor-Pro Lexer Package

The lexer converts raw PDF lines into semantic tokens.

Pipeline:

Raw PDF Lines
        ¦
        ?
     Lexer
        ¦
        ?
     Token[]
        ¦
        ?
Question Parser
Section Parser
Table Parser
Formula Parser
"""

from .token import Token
from .tokens import TokenType
from .lexer import Lexer

__all__ = [
    "Lexer",
    "Token",
    "TokenType",
]