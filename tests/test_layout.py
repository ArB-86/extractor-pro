from doclayout_yolo import YOLOv10

MODEL_PATH = (
    "/home/jiitcah.05/.cache/huggingface/hub/"
    "models--juliozhao--DocLayout-YOLO-DocStructBench/"
    "snapshots/8c3299a30b8ff29a1503c4431b035b93220f7b11/"
    "doclayout_yolo_docstructbench_imgsz1024.pt"
)

model = YOLOv10(MODEL_PATH)

results = model.predict(
    source="data/rendered/fegp101/page_001.png",
    imgsz=1024,
    conf=0.2,
    save=True,
)

print(results)