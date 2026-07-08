import json
from pathlib import Path


class JSONWriter:

    @staticmethod
    def write(region):

        path = Path(region.image_path)

        json_path = path.with_suffix(".json")

        data = {

            "page": region.page,

            "label": region.label,

            "confidence": float(region.confidence),

            "bbox": [

                float(region.x1),
                float(region.y1),
                float(region.x2),
                float(region.y2),

            ],

            "image_path": region.image_path,

            "text": region.text,

        }

        with open(json_path, "w") as f:

            json.dump(data, f, indent=4)
