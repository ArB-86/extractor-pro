
from pathlib import Path

from src.pipeline.production_pipeline import ProductionPipeline


class Extractor:

    def __init__(self):

        self.pipeline = ProductionPipeline()

    def extract(
        self,
        pdf_path,
        output_dir,
    ):

        output_dir = Path(output_dir)

        output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        return self.pipeline.run(
            pdf_path,
            str(output_dir),
        )
