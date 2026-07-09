from pathlib import Path

from src.pipeline.document_pipeline import DocumentPipeline


class Extractor:

    def __init__(self):

        self.pipeline = DocumentPipeline()

    def extract(
        self,
        pdf_path: str,
        output_dir: str,
    ):

        output_dir = Path(output_dir)

        output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        master_return self.pipeline.run(
            pdf_path=pdf_path,
            output_dir=str(output_dir),
        )

        return master_dataset

