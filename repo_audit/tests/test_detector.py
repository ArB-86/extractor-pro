from src.layout.doclayout_yolo import DocLayoutYOLO

detector = DocLayoutYOLO()

results = detector.detect(
    "data/rendered/fegp101/page_001.png"
)

print(results)
