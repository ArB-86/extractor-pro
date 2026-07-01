import pytest

from pipeline.classifiers.question_classifier import QuestionClassifier
from pipeline.models import Paragraph, BlockType


@pytest.mark.parametrize(
    "text,number,starred",
    [
        ("1. Find x.", 1, False),
        ("12. Solve.", 12, False),
        ("99. Compute.", 99, False),
        ("*7. HOTS.", 7, True),
        ("*15. Challenge.", 15, True),
    ],
)
def test_question_metadata(text, number, starred):

    block = Paragraph(
        page=1,
        bbox=(0,0,0,0),
        text=text,
    )

    QuestionClassifier().classify([block])

    assert block.block_type == BlockType.QUESTION
    assert block.metadata["question_no"] == number
    assert block.metadata["starred"] == starred
