
import time


class PipelineEngine:

    def __init__(self, stages):

        self.stages = stages

    def run(self, context):

        context.metrics.setdefault("stage_times", {})

        for stage in self.stages:

            t0 = time.perf_counter()

            context = stage.run(context)

            dt = time.perf_counter() - t0

            context.metrics["stage_times"][
                stage.__class__.__name__
            ] = round(dt, 4)

        return context
