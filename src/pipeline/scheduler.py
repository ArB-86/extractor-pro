from src.pipeline.hpc_pipeline import HPCPipeline


class Scheduler:

    def run(self, pdfs, output_dir):

        hpc = HPCPipeline()

        for pdf in pdfs:

            hpc.submit(
                pdf,
                output_dir,
            )
