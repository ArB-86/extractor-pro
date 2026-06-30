from pipeline.classifiers.question_classifier import QuestionClassifier
from pipeline.models import Paragraph, BlockType


def test_question_detection():

    block = Paragraph(
        page=1,
        bbox=(0,0,0,0),
        text="12. Find the value of x."
    )

    QuestionClassifier().classify([block])

    assert block.block_type == BlockType.QUESTION
