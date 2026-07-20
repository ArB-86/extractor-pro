from __future__ import annotations

import re

from src.schema.region import Region


class RegionQualityFilter:

    PAGE = re.compile(r"(page\s*no|d\s*age|\bage\b)", re.I)

    SUMMARY = re.compile(
        r"u?mm\s*2?\s*r\s*y|summary",
        re.I,
    )

    TINY = re.compile(r"^[A-Za-z]{1,3}$")

    @classmethod
    def keep(cls, region: Region) -> bool:

        text = (region.text or "").strip()

        if not text:
            return False

        compact = re.sub(r"\s+", "", text.lower())

        if cls.PAGE.search(compact):
            return False

        if cls.SUMMARY.search(compact):
            return False

        if cls.TINY.fullmatch(compact):
            return False

        return True
