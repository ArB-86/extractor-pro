from src.dataset.registry import QuestionRegistry
from src.dataset.manifest import DatasetManifest
from src.dataset.statistics import DatasetStatistics
from src.storage.jsonl_store import JSONLStore
from src.storage.parquet_store import ParquetStore
from src.storage.sqlite_store import SQLiteStore
from src.search.index import SearchIndex


class MasterDataset:

    def __init__(self):

        self.registry = QuestionRegistry()

        self.manifest = DatasetManifest()

        self.statistics = DatasetStatistics()

        self.jsonl = JSONLStore()

        self.parquet = ParquetStore()

        self.sqlite = SQLiteStore()

        self.index = SearchIndex()

    def add(self, questions):

        self.registry.extend(questions)

    def export(self, output_dir):

        questions = self.registry.all()

        self.jsonl.write(
            questions,
            f"{output_dir}/master_dataset.jsonl",
        )

        self.parquet.write(
            questions,
            f"{output_dir}/master_dataset.parquet",
        )

        self.sqlite.write(
            questions,
            f"{output_dir}/master_dataset.sqlite",
        )

        return {
            "manifest": self.manifest.build(questions),
            "statistics": self.statistics.build(questions),
            "search_index": self.index.build(questions),
        }
