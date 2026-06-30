from pipeline.hierarchy.builder import HierarchyBuilder
from pipeline.models import Paragraph, BlockType


def test_exercise_tree():

    exercise = Paragraph(
        page=1,
        bbox=(0,0,0,0),
        text="Exercise 2.3",
        block_type=BlockType.EXERCISE,
    )

    q1 = Paragraph(
        page=1,
        bbox=(0,0,0,0),
        text="1. Find...",
        block_type=BlockType.QUESTION,
    )

    q2 = Paragraph(
        page=1,
        bbox=(0,0,0,0),
        text="2. Solve...",
        block_type=BlockType.QUESTION,
    )

    tree = HierarchyBuilder().build([
        exercise,
        q1,
        q2,
    ])

    exercise_node = tree.children[0]

    assert exercise_node.block.block_type == BlockType.EXERCISE
    assert len(exercise_node.children) == 2
