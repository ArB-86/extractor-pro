import copy
import re

# Looks like "2. Find ..."
FAKE_CONTINUATION = re.compile(r"^2\.\s+[A-Z][a-z]")

# Formula blocks: lines containing numbers, letters, operators, parentheses, etc.
FORMULA_BLOCK = re.compile(
    r"^[0-9A-Za-z°α-ωΑ-Ωθφπ+\-=/().,\s²³]+$",
    re.MULTILINE,
)


class BlockMerger:

    def __init__(self, blocks):
        self.blocks = blocks

    def process(self):

        if not self.blocks:
            return []

        merged = [copy.copy(self.blocks[0])]

        for block in self.blocks[1:]:

            prev = merged[-1]

            text = block.text.strip()

            # -------------------------------------------------
            # OCR bug:
            #
            # 22176 m
            # 2. Find ...
            #
            # or
            #
            # 770 cm
            # 2. Find ...
            #
            # where the "2." is actually the lost superscript ²
            # -------------------------------------------------

            if (
                FAKE_CONTINUATION.match(text)
                and (
                    prev.text.rstrip().endswith(" m")
                    or prev.text.rstrip().endswith(" cm")
                )
            ):
                prev.text += "² " + text[2:].lstrip()
                continue

            # -------------------------------------------------
            # Formula block printed just before "12. Prove that"
            # or "13. Show that"
            # -------------------------------------------------
            if (
                text.startswith(("12. Prove that", "13. Show that"))
                and len(merged) >= 1
            ):
                prev = merged[-1]

                if (
                    FORMULA_BLOCK.match(prev.text.strip())
                    and not re.match(r"^\d+\.", prev.text.strip())
                ):
                    # Move the formula from the previous block into the current one
                    current = copy.copy(block)
                    current.text += "\n" + prev.text
                    merged[-1] = current
                    continue

            # Default: append the block as is
            merged.append(copy.copy(block))

        return merged