from pipeline.hierarchy.builder import HierarchyBuilder
from pipeline.models import Paragraph, BlockType


def test_subquestion_tree():

    exercise = Paragraph(
        page=1,
        bbox=(0, 0, 0, 0),
        text="Exercise 2.3",
        block_type=BlockType.EXERCISE,
    )

    question = Paragraph(
        page=1,
        bbox=(0, 0, 0, 0),
        text="1. Find...",
        block_type=BlockType.QUESTION,
    )

    sub1 = Paragraph(
        page=1,
        bbox=(0, 0, 0, 0),
        text="(i) First",
        block_type=BlockType.SUBQUESTION,
    )

    sub2 = Paragraph(
        page=1,
        bbox=(0, 0, 0, 0),
        text="(ii) Second",
        block_type=BlockType.SUBQUESTION,
    )

    tree = HierarchyBuilder().build([
        exercise,
        question,
        sub1,
        sub2,
    ])

    qnode = tree.children[0].children[0]

    assert len(qnode.children) == 2
