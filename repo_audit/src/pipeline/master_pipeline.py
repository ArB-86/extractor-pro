from src.dataset.master_dataset import MasterDataset
from src.pipeline.batch_pipeline import BatchPipeline  # new import


class MasterPipeline:

    def __init__(self):
        self.dataset = MasterDataset()

    def run(self, pdfs, output_dir):

        # Run batch processing on all PDFs
        results = BatchPipeline().run(
            pdfs,
            output_dir,
        )

        for result in results:

            self.dataset.add(
                result.questions,
            )

        return self.dataset.export(
            output_dir,
        )
