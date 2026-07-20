from pipeline.classifiers.exercise_classifier import ExerciseClassifier
from pipeline.models import Paragraph, BlockType


def test_exercise_detection():

    block = Paragraph(
        page=1,
        bbox=(0,0,0,0),
        text="Exercise 2.3"
    )

    ExerciseClassifier().classify([block])

    assert block.block_type == BlockType.EXERCISE
