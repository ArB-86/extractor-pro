from __future__ import annotations

from pipeline.models import BlockType

from .node import Node


class HierarchyBuilder:

    def build(self, blocks):

        root = Node(block=None)

        current_exercise = None
        current_question = None

        for block in blocks:

            node = Node(block=block)

            if block.block_type == BlockType.EXERCISE:

                root.add(node)
                current_exercise = node
                current_question = None

            elif block.block_type == BlockType.QUESTION:

                current_question = node

                if current_exercise is not None:
                    current_exercise.add(node)
                else:
                    root.add(node)

            elif block.block_type == BlockType.SUBQUESTION:

                if current_question is not None:
                    current_question.add(node)
                else:
                    root.add(node)

            else:

                root.add(node)

        return root