from __future__ import annotations

from dataclasses import asdict
from hashlib import sha256
from pathlib import Path
import json
from typing import Iterable

from src.document.question import Question


class DatasetBuilder:
    """
    Legacy compatibility wrapper.

    Production dataset creation is handled by MasterDataset.
    """

    def __init__(self):
        from src.dataset.master_dataset import MasterDataset
        self.dataset = MasterDataset()

    def add(self, question):
        self.dataset.add([question])

    def extend(self, questions):
        self.dataset.add(questions)

    def build(self):
        return self.dataset

    def export_json(self, output):
        return self.dataset.export(output)
