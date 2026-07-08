from PIL import Image


class SuryaOCR:

    def __init__(self):
        self.model = None

    def _lazy_load(self):
        if self.model is not None:
            return

        from surya.recognition import RecognitionPredictor

        self.model = RecognitionPredictor()

    def recognize(self, image_path: str):

        self._lazy_load()

        image = Image.open(image_path).convert("RGB")

        predictions = self.model([image])

        lines = []

        for line in predictions[0].text_lines:
            lines.append(line.text)

        return "\n".join(lines)
