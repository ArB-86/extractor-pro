from __future__ import annotations

import re

from src.schema.region import Region


class RegionRepair:

    TITLE_GAP = 40
    PARAGRAPH_GAP = 18

    def repair(self, regions):

        if not regions:
            return []

        repaired = []

        i = 0

        while i < len(regions):

            r = regions[i]

            self._clean_text(r)

            while (
                i + 1 < len(regions)
                and self._can_merge(r, regions[i + 1])
            ):

                nxt = regions[i + 1]

                self._merge(r, nxt)

                i += 1

            repaired.append(r)

            i += 1

        return repaired

    def _clean_text(self, region):

        if not region.text:
            return

        t = region.text

        t = t.replace("-\n", "")
        t = re.sub(r"\n+", "\n", t)
        t = re.sub(r"[ \t]+", " ", t)
        t = re.sub(r"\s+([.,;:!?])", r"\1", t)

        region.text = t.strip()

    def _can_merge(self, a, b):

        if a.page != b.page:
            return False

        if a.label != b.label:
            return False

        if a.label == "title":

            return abs(b.y1 - a.y2) <= self.TITLE_GAP

        if a.label == "plain_text":

            return abs(b.y1 - a.y2) <= self.PARAGRAPH_GAP

        return False

    def _merge(self, a, b):

        if a.text and b.text:
            a.text += "\n" + b.text

        elif b.text:
            a.text = b.text

        a.x1 = min(a.x1, b.x1)
        a.y1 = min(a.y1, b.y1)
        a.x2 = max(a.x2, b.x2)
        a.y2 = max(a.y2, b.y2)
