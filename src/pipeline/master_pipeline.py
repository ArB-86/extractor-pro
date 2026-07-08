from src.extractor.extractor import Extractor
from src.dataset.master_dataset import MasterDataset
from src.pipeline.batch_pipeline import BatchPipeline  # new import


class MasterPipeline:

    def __init__(self):

        self.extractor = Extractor()

        self.dataset = MasterDataset()

    def run(self, pdfs, output_dir):

        # Run batch processing on all PDFs
        results = BatchPipeline().run(
            pdfs,
            output_dir,
        )

        # Add all results to the master dataset
        for questions in results:
            self.dataset.add(questions)

        return self.dataset.export(output_dir)
