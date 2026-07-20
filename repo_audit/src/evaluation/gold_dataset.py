from __future__ import annotations

from pathlib import Path

from .gold_loader import GoldDatasetLoader
from .gold_validator import GoldDatasetValidator
from .dataset_converter import DatasetConverter
from .dataset_manifest import DatasetManifest
from .dataset_integrity import DatasetIntegrity


class GoldDataset:

    def __init__(self):

        self.loader = GoldDatasetLoader()

        self.validator = GoldDatasetValidator()

        self.converter = DatasetConverter()

        self.integrity = DatasetIntegrity()

    def load(

        self,

        path,

    ):

        return self.loader.load(path)

    def validate(

        self,

        rows,

    ):

        return self.validator.validate(rows)

    def manifest(

        self,

        rows,

        name="gold",

        version="1.0",

    ):

        return DatasetManifest(

            dataset_name=name,

            version=version,

            total_questions=len(rows),

            books=[],

            files=[],

        ).compute()

    def statistics(

        self,

        rows,

    ):

        return self.integrity.statistics(rows)
