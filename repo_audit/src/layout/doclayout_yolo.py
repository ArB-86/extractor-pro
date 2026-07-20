from pathlib import Path

from doclayout_yolo import YOLOv10


MODEL_PATH = (
    Path.home()
    / ".cache"
    / "huggingface"
    / "hub"
    / "models--juliozhao--DocLayout-YOLO-DocStructBench"
    / "snapshots"
    / "8c3299a30b8ff29a1503c4431b035b93220f7b11"
    / "doclayout_yolo_docstructbench_imgsz1024.pt"
)


class DocLayoutYOLO:

    def __init__(self):

        self.model = YOLOv10(str(MODEL_PATH))

    def detect(self, image_path):

        return self.model.predict(
            source=str(image_path),
            imgsz=1024,
            conf=0.20,
            verbose=False,
        )