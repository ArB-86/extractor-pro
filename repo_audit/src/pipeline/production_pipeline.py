from src.pipeline.document_pipeline import DocumentPipeline
from src.pipeline.validation_pipeline import ValidationPipeline
from src.dataset.master_dataset import MasterDataset
from src.pipeline.evaluation_pipeline import EvaluationPipeline


class ProductionPipeline:

    def __init__(self):

        self.document = DocumentPipeline()

        self.validation = ValidationPipeline()
        self.evaluation = EvaluationPipeline()

    def run(
        self,
        pdf_path,
        output_dir,
        gold_path=None,
    ):

        dataset = self.document.run(
            pdf_path,
            output_dir,
        )

        print(f"[ProductionPipeline] dataset questions: {len(dataset.questions())}")

        result = dataset.export(
            output_dir,
        )

        return self.evaluation.run(
            result,
            gold_path,
        )
