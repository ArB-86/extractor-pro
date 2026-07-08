from concurrent.futures import ProcessPoolExecutor

from src.extractor.extractor import Extractor


class BatchPipeline:

    def __init__(self, workers=8):

        self.workers = workers

    @staticmethod
    def _run(job):

        pdf, output = job

        return Extractor().extract(
            pdf_path=pdf,
            output_dir=output,
        )

    def run(self, pdfs, output_dir):

        jobs = [
            (pdf, output_dir)
            for pdf in pdfs
        ]

        with ProcessPoolExecutor(
            max_workers=self.workers
        ) as executor:

            return list(
                executor.map(
                    self._run,
                    jobs,
                )
            )
