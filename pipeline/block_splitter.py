import copy
import re

QUESTION_INSIDE = re.compile(r"\n([1-9][0-9]*)\.\s")


class BlockSplitter:

    def __init__(self, blocks):
        self.blocks = blocks

    def process(self):

        result = []

        for block in self.blocks:

            text = block.text

            m = QUESTION_INSIDE.search(text)

            if not m:
                result.append(block)
                continue

            before = copy.copy(block)
            after = copy.copy(block)

            before.text = text[:m.start()].strip()
            after.text = text[m.start() + 1:].strip()

            if before.text:
                result.append(before)

            if after.text:
                result.append(after)

        return result
