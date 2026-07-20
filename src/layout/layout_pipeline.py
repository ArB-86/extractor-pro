from pathlib import Path

from src.crop.cropper import Cropper
from src.io.json_writer import JSONWriter
from src.layout.doclayout_yolo import DocLayoutYOLO
from src.layout.filter import LayoutFilter
from src.layout.layout_parser import LayoutParser
from src.ocr.factory import OCRFactory
from src.reading_order.sorter import ReadingOrderSorter
from src.schema.region import Region
from src.utils.thread_pool import parallel_map
from src.ocr.postprocess import OCRPostProcessor
from src.ocr.language_repair import OCRLanguageRepair  # added


class LayoutPipeline:

    def __init__(self):
        self.detector = DocLayoutYOLO()
        self.parser = LayoutParser()
        self.filter = LayoutFilter()
        self.cropper = Cropper()

    def _process(self, item, image_path, output_dir, page):
        i, box = item

        img = self.cropper.crop(image_path, box)

        label = box.label.replace(" ", "_")

        filename = f"{i:03d}_{label}_{box.confidence:.2f}.png"

        save_path = output_dir / filename

        img.save(save_path)

        ocr = OCRFactory.get(label)

        text = ocr.recognize(str(save_path))
        text = OCRPostProcessor.clean(text)
        text = OCRLanguageRepair.repair(text)   # <-- added

        region = Region(

            page=page,

            label=label,

            confidence=box.confidence,

            x1=box.x1,
            y1=box.y1,
            x2=box.x2,
            y2=box.y2,

            image_path=str(save_path),

            text=text,
        )

        JSONWriter.write(region)

        return region

    def run(self, image_path: str, output_dir: str, page: int = 1, workers: int = 8):
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        results = self.detector.detect(image_path)

        boxes = self.parser.parse(results[0])
        boxes = self.filter.filter(boxes)

        regions = parallel_map(
            lambda item: self._process(item, image_path, output_dir, page),
            list(enumerate(boxes)),
            workers=workers,
        )

        regions = ReadingOrderSorter.sort(regions)
        return regions
