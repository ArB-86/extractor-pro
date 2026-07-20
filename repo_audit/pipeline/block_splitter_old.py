import copy
import re

QUESTION_INSIDE = re.compile(r"\n([1-9][0-9]*)\.\s")


class BlockSplitter:

    def __init__(self, blocks):
        self.blocks = blocks

    def process(self):

        result = list(self.blocks)
        changed = True

        while changed:
            changed = False
            new_result = []

            for block in result:

                text = block.text
                m = QUESTION_INSIDE.search(text)

                if not m:
                    new_result.append(block)
                    continue

                changed = True
                before = copy.copy(block)
                after = copy.copy(block)

                before.text = text[:m.start()].strip()
                after.text = text[m.start() + 1:].strip()

                if before.text:
                    new_result.append(before)

                if after.text:
                    new_result.append(after)

            result = new_result

        return result
