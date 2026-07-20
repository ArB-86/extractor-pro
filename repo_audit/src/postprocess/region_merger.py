from typing import List

from src.schema.region import Region


class RegionMerger:

    @staticmethod
    def merge(regions: List[Region]) -> List[Region]:

        if not regions:
            return []

        merged = []

        current = regions[0]

        for nxt in regions[1:]:

            # Only merge consecutive plain text regions
            if (
                current.label == "plain_text"
                and nxt.label == "plain_text"
            ):

                current.text += "\n" + nxt.text

                current.x1 = min(current.x1, nxt.x1)
                current.y1 = min(current.y1, nxt.y1)
                current.x2 = max(current.x2, nxt.x2)
                current.y2 = max(current.y2, nxt.y2)

                continue

            merged.append(current)
            current = nxt

        merged.append(current)

        return merged
