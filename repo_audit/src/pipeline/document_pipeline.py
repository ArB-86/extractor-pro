from src.extractor.extractor import Extractor
from src.dataset.master_dataset import MasterDataset
from src.pipeline.batch_pipeline import BatchPipeline
from src.validation.validator import Validator


class DocumentPipeline:
    """Pipeline for processing individual documents."""

    def __init__(self):
        self.extractor = Extractor()
        self.dataset = MasterDataset()
        self.validation = Validator()

    def run(self, pdf_path, output_dir):
        """Process a single PDF document."""
        print(f"[DocumentPipeline] Processing: {pdf_path}")

        # Extract questions from the PDF
        questions = self.extractor.extract(
            pdf_path=pdf_path,
            output_dir=output_dir,
        )

        print(f"[DocumentPipeline] extracted: {len(questions)}")

        # Validate the extracted questions
        questions = self.validation.run(
            questions
        )

        print(
            "[DocumentPipeline] validation type:",
            type(questions),
        )

        questions = list(questions)

        print(
            f"[DocumentPipeline] after validation: {len(questions)}"
        )

        # Add validated questions to the dataset
        self.dataset.extend(
            questions
        )

        return questions

    def run_batch(self, pdfs, output_dir):
        """Process multiple PDF documents in batch."""
        results = BatchPipeline().run(
            pdfs,
            output_dir,
        )

        for questions in results:
            # Validate each batch of questions
            questions = self.validation.run(
                questions
            )

            print(
                "[DocumentPipeline] validation type:",
                type(questions),
            )

            questions = list(questions)

            print(
                f"[DocumentPipeline] after validation: {len(questions)}"
            )

            self.dataset.extend(
                questions
            )

        return self.dataset.export(output_dir)
