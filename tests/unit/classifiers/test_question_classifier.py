import pytest

from pipeline.classifiers.question_classifier import QuestionClassifier
from pipeline.models import Paragraph, BlockType


@pytest.mark.parametrize(
    "text,expected",
    [

        ("1. Find x.", True),
        ("2. Solve.", True),
        ("15. Evaluate.", True),
        ("99. Compute.", True),
        ("*7. Challenge.", True),
        ("*15. HOTS.", True),

        ("12.5 cm", False),
        ("2026.", False),
        ("Exercise 2.3", False),
        ("Example 4", False),
        ("Activity", False),
        ("Figure it Out", False),
        ("Table 2.1", False),
        ("Fig. 2.3", False),
        ("Chapter 3", False),
        ("Polynomial", False),
        ("(i)", False),
        ("(ii)", False),
        ("(a)", False),
        ("(b)", False),
        ("Let us solve", False),
        ("NCERT", False),
        ("Summary", False),
        ("Think", False),
        ("Observe", False),
        ("Solution", False),
        ("Proof", False),
        ("Hint", False),
        ("Theorem", False),
        ("Definition", False),

    ],
)
def test_question_classifier(text, expected):

    block = Paragraph(
        page=1,
        bbox=(0,0,0,0),
        text=text,
    )

    QuestionClassifier().classify([block])

    assert (block.block_type == BlockType.QUESTION) == expected
