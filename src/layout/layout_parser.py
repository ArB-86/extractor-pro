from .layout_schema import LayoutBox


class LayoutParser:

    def parse(self, result):

        output = []

        boxes = result.boxes

        for box in boxes:

            cls = int(box.cls.item())

            conf = float(box.conf.item())

            x1, y1, x2, y2 = box.xyxy[0].tolist()

            label = result.names[cls]

            output.append(

                LayoutBox(
                    label=label,
                    confidence=conf,
                    x1=x1,
                    y1=y1,
                    x2=x2,
                    y2=y2,
                )

            )

        return output
