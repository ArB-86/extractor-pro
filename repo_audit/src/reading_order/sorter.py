from typing import List

from src.schema.region import Region


class ReadingOrderSorter:

    @staticmethod
    def sort(regions: List[Region]) -> List[Region]:
        """
        Top-to-bottom, then left-to-right.
        """

        return sorted(
            regions,
            key=lambda r: (
                r.page,
                r.y1,
                r.x1,
            ),
        )
