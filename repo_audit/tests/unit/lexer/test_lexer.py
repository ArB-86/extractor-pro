from pipeline.lexer.lexer import Lexer
from pipeline.models import Paragraph


def test_empty():

    lexer = Lexer()

    block = Paragraph(
        page=1,
        bbox=(0, 0, 0, 0),
        text=""
    )

    assert lexer.tokenize(block) == []
