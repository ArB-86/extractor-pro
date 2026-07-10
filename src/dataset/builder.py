from __future__ import annotations

from src.dataset.master_dataset import MasterDataset


class DatasetBuilder:

    def __init__(self):
        self.dataset = MasterDataset()

    def add(self, question):
        print("[DatasetBuilder] add 1")
        self.dataset.add([question])

    def extend(self, questions):
        questions = list(questions)

        print(f"[DatasetBuilder] extend {len(questions)}")

        self.dataset.add(questions)

        print(
            f"[DatasetBuilder] after add: "
            f"{len(self.dataset.questions())}"
        )

    def build(self):
        print(
            f"[DatasetBuilder] build: "
            f"{len(self.dataset.questions())}"
        )
        return self.dataset

    def export_json(self, output):
        return self.dataset.export(output)
