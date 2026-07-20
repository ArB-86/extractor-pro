from pipeline.hierarchy.builder import HierarchyBuilder
from pipeline.models import Paragraph


def test_build():

    blocks = [
        Paragraph(page=1, bbox=(0,0,0,0), text="A"),
        Paragraph(page=1, bbox=(0,0,0,0), text="B"),
    ]

    tree = HierarchyBuilder().build(blocks)

    assert len(tree.children) == 2
