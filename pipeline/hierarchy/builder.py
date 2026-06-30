from __future__ import annotations

from pipeline.models import BlockType

from .node import Node


class HierarchyBuilder:

    def build(self, blocks):

        root = Node(block=None)

        current_exercise = None

        for block in blocks:

            node = Node(block=block)

            if block.block_type == BlockType.EXERCISE:

                root.add(node)
                current_exercise = node

            elif (
                block.block_type == BlockType.QUESTION
                and current_exercise is not None
            ):

                current_exercise.add(node)

            else:

                root.add(node)

        return root
