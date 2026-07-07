from pathlib import Path

from src.crop.cropper import Cropper
from src.layout.doclayout_yolo import DocLayoutYOLO
from src.layout.layout_parser import LayoutParser
from src.layout.filter import LayoutFilter

IMAGE = "data/rendered/fegp101/page_001.png"

OUTPUT_DIR = Path("debug/crops")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

detector = DocLayoutYOLO()
parser = LayoutParser()
layout_filter = LayoutFilter()
cropper = Cropper()

results = detector.detect(IMAGE)

boxes = parser.parse(results[0])
boxes = layout_filter.filter(boxes)

print(f"\nDetected {len(boxes)} valid regions\n")

for i, box in enumerate(boxes):

    img = cropper.crop(IMAGE, box)

    label = box.label.replace(" ", "_")

    filename = (
        f"{i:03d}_{label}_{box.confidence:.2f}.png"
    )

    save_path = OUTPUT_DIR / filename

    img.save(save_path)

    print(save_path)

print("\nDone.")