
from src.pipeline.document_pipeline import DocumentPipeline
from src.pipeline.validation_pipeline import ValidationPipeline
from src.dataset.master_dataset import MasterDataset


class ProductionPipeline:

    def __init__(self):

        self.document = DocumentPipeline()

        self.validation = ValidationPipeline()

    def run(
        self,
        pdf_path,
        output_dir,
    ):

        questions = self.document.run(
            pdf_path,
            output_dir,
        )

        questions = self.validation.run(
            questions,
        )

        dataset = MasterDataset()

        dataset.add(
            questions,
        )

        return dataset.export(
            output_dir,
        )
