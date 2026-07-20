from src.document.document import Document
from src.postprocess.region_merger import RegionMerger
from src.reading_order.geometry_sorter import GeometrySorter
from src.text.cleaner import TextCleaner
from src.postprocess.region_quality import RegionQualityFilter


class DocumentBuilder:

    @staticmethod
    def build(regions):

        if not regions:
            return Document(
                pages=0,
                regions=[],
            )

        regions = GeometrySorter.sort(regions)

        if not regions:
            return Document(
                pages=0,
                regions=[],
            )

        # ---- Stable ordering: titles first on each page ----
        regions.sort(
            key=lambda r: (
                r.page,
                r.y1,
                0 if r.label == "title" else 1,
                r.x1,
            )
        )

        regions = RegionMerger.merge(regions)

        if not regions:
            return Document(
                pages=0,
                regions=[],
            )

        cleaned = []

        for r in regions:

            if not RegionQualityFilter.keep(r):
                continue

            if r.text:
                r.text = TextCleaner.clean(r.text)

            cleaned.append(r)

        if not cleaned:
            return Document(
                pages=0,
                regions=[],
            )

        return Document(
            pages=max(r.page for r in cleaned),
            regions=cleaned,
        )
