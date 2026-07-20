from pipeline.classifiers.question_classifier import QuestionClassifier
from pipeline.models import Paragraph


def test_question_text():

    block = Paragraph(
        page=1,
        bbox=(0,0,0,0),
        text="12. Find the value of x.",
    )

    QuestionClassifier().classify([block])

    assert block.metadata["question_text"] == "Find the value of x."
    assert block.metadata["question_prefix"] == "12."
