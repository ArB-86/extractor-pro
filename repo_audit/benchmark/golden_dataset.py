
from __future__ import annotations

import json


class GoldenDataset:

    def load(self, path):

        with open(path, encoding="utf8") as f:
            return json.load(f)

    def save(self, data, path):

        with open(path, "w", encoding="utf8") as f:
            json.dump(
                data,
                f,
                indent=4,
                ensure_ascii=False
            )
