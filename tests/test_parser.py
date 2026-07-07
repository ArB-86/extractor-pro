from src.layout.doclayout_yolo import DocLayoutYOLO
from src.layout.layout_parser import LayoutParser

detector = DocLayoutYOLO()

parser = LayoutParser()

results = detector.detect(
    "data/rendered/fegp101/page_001.png"
)

boxes = parser.parse(results[0])

print()

print("=" * 80)

print(f"Detected {len(boxes)} objects\n")

for b in boxes:

    print(b)
