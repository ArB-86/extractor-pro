
from src.pipeline.incremental_pipeline import IncrementalPipeline


class BatchPipeline:

    def __init__(self):

        self.pipeline = IncrementalPipeline()

    def run(
        self,
        pdfs,
        output_dir,
        gold_path=None,
    ):

        return self.pipeline.run(
            pdfs,
            output_dir,
            gold_path,
        )
