from rapidocr_onnxruntime import RapidOCR


class RapidOCREngine:

    def __init__(self):
        self.engine = RapidOCR()

    def recognize(self, image_path: str):

        result, _ = self.engine(image_path)

        if result is None:
            return ""

        lines = []

        for item in result:
            lines.append(item[1])

        return "\n".join(lines)
