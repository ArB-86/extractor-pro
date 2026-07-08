from src.extractor.extractor import Extractor
from src.dataset.master_dataset import MasterDataset


class MasterPipeline:

    def __init__(self):

        self.extractor = Extractor()

        self.dataset = MasterDataset()

    def run(self, pdfs, output_dir):

        for pdf in pdfs:

            questions = self.extractor.extract(
                pdf_path=pdf,
                output_dir=output_dir,
            )

            self.dataset.add(questions)

        return self.dataset.export(output_dir)
