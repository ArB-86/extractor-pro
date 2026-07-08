from src.document.document import Document
from src.postprocess.region_merger import RegionMerger
from src.reading_order.geometry_sorter import GeometrySorter
from src.text.cleaner import TextCleaner   # new import


class DocumentBuilder:

    @staticmethod
    def build(regions):
        regions = GeometrySorter.sort(regions)
        regions = RegionMerger.merge(regions)

        pages = max(r.page for r in regions)

        doc = Document(pages=pages)

        # Clean text for all regions before adding to document
        for r in regions:
            r.text = TextCleaner.clean(r.text)

        for r in regions:
            doc.add_region(r)

        return doc