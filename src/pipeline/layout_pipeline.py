from pathlib import Path

from src.crop.cropper import Cropper
from src.io.json_writer import JSONWriter
from src.layout.doclayout_yolo import DocLayoutYOLO
from src.layout.filter import LayoutFilter
from src.layout.layout_parser import LayoutParser
from src.ocr.factory import OCRFactory
from src.reading_order.sorter import ReadingOrderSorter
from src.schema.region import Region


class LayoutPipeline:

    def __init__(self):
        self.detector = DocLayoutYOLO()
        self.parser = LayoutParser()
        self.filter = LayoutFilter()
        self.cropper = Cropper()

    def run(self, image_path: str, output_dir: str, page: int = 1):
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        results = self.detector.detect(image_path)

        boxes = self.parser.parse(results[0])

        # ---- DEBUG: Raw boxes ----
        print("=" * 80)
        print("RAW BOXES")
        for i, b in enumerate(boxes):
            print(
                i,
                b.label,
                round(b.confidence, 3),
                (b.x1, b.y1, b.x2, b.y2),
            )
        print("=" * 80)

        boxes = self.filter.filter(boxes)

        # ---- DEBUG: Filtered boxes ----
        print("=" * 80)
        print("FILTERED BOXES")
        for i, b in enumerate(boxes):
            print(
                i,
                b.label,
                round(b.confidence, 3),
                (b.x1, b.y1, b.x2, b.y2),
            )
        print("=" * 80)

        print(f"[Layout] Page {page}: {len(boxes)} boxes")

        regions = []

        for i, box in enumerate(boxes):
            img = self.cropper.crop(image_path, box)

            label = box.label.replace(" ", "_")

            filename = f"{i:03d}_{label}_{box.confidence:.2f}.png"

            save_path = output_dir / filename

            img.save(save_path)

            ocr = OCRFactory.get(label)

            print(f"[OCR] {i + 1}/{len(boxes)}  {label}")

            text = ocr.recognize(str(save_path))

            print(f"[OCR] done ({len(text)} chars)")

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

            regions.append(region)

        # Sort regions by reading order before returning
        regions = ReadingOrderSorter.sort(regions)
        return regions
