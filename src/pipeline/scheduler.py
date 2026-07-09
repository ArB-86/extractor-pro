from src.pipeline.hpc_pipeline import HPCPipeline


class Scheduler:

    def run(self, pdfs, output_dir):

        hpc = HPCPipeline()

        jobs = []

        for pdf in pdfs:

            jobs.append(

                hpc.submit(
                    pdf,
                    output_dir,
                )

            )

        return jobs
