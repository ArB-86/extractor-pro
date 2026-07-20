from typing import List

from src.schema.region import Region


class GeometrySorter:

    @staticmethod
    def sort(regions: List[Region]) -> List[Region]:
        """
        Stable top-to-bottom, then left-to-right ordering.
        Regions on nearly the same horizontal line are grouped together.
        """

        tolerance = 40

        regions = sorted(regions, key=lambda r: r.y1)

        rows = []

        for region in regions:
            if not rows:
                rows.append([region])
                continue

            last_row = rows[-1]

            if abs(region.y1 - last_row[0].y1) <= tolerance:
                last_row.append(region)
            else:
                rows.append([region])

        ordered = []

        for row in rows:
            row.sort(key=lambda r: r.x1)
            ordered.extend(row)

        return ordered
