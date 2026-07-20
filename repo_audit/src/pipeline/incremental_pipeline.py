
from src.pipeline.production_pipeline import ProductionPipeline


class IncrementalPipeline:

    def __init__(self):

        self.pipeline = ProductionPipeline()

    def run(
        self,
        pdfs,
        output_dir,
        gold_path=None,
    ):

        results = []

        for pdf in pdfs:

            results.append(

                self.pipeline.run(
                    pdf_path=str(pdf),
                    output_dir=output_dir,
                    gold_path=gold_path,
                )

            )

        return results
