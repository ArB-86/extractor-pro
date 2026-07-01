from __future__ import annotations

import copy
import re

_ISOLATED_NUMBER = re.compile(r"^\d+\.\s*$")


class BlockNormalizer:

  def __init__(self, blocks):
    self.blocks = blocks

  def process(self):
    merged = self._merge_isolated_numbers(self.blocks)
    return self._merge_continued_lines(merged)

  def _merge_isolated_numbers(self, blocks):
    result = []
    i = 0

    while i < len(blocks):
      block = blocks[i]
      text = block.text.strip()

      if _ISOLATED_NUMBER.match(text) and i + 1 < len(blocks):
        nxt = blocks[i + 1]
        combined = copy.copy(block)
        combined.text = f"{text} {nxt.text.strip()}"
        combined.bbox = (
          min(block.bbox[0], nxt.bbox[0]),
          min(block.bbox[1], nxt.bbox[1]),
          max(block.bbox[2], nxt.bbox[2]),
          max(block.bbox[3], nxt.bbox[3]),
        )
        combined.page = block.page
        result.append(combined)
        i += 2
        continue

      result.append(block)
      i += 1

    return result

  def _merge_continued_lines(self, blocks):
    """Join blocks that are only a continuation line (e.g. formula fragments)."""
    if not blocks:
      return []

    merged = [copy.copy(blocks[0])]

    for block in blocks[1:]:
      text = block.text.strip()
      prev = merged[-1]

      if (
        text
        and len(text) < 80
        and not re.match(r"^\d+\.", text)
        and not re.match(r"^\([A-E]\)", text, re.I)
        and (
          prev.text.rstrip().endswith(
            ("=", "+", "-", "/", "×", "·", "(", "[", "{", ":")
          )
          or text.startswith((")", "]", "}", ",", ".", "%"))
          or text[:1].islower()
        )
      ):
        prev.text = prev.text.rstrip() + " " + text
        continue

      merged.append(copy.copy(block))

    return merged
