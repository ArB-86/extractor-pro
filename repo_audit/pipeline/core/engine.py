
from __future__ import annotations

import time
from pathlib import Path


def _stage_name(stage) -> str:
    return stage.__class__.__name__


class PipelineEngine:

    def __init__(self, stages):

        self.stages = stages

    def run(self, context, debug_dir: str | Path | None = None):

        context.metrics.setdefault("stage_times", {})

        debugger = None

        if debug_dir is not None:
            from pipeline.core.debug_dump import PipelineDebugger

            debugger = PipelineDebugger(Path(debug_dir), context.pdf)

        for stage in self.stages:

            t0 = time.perf_counter()

            context = stage.run(context)

            dt = time.perf_counter() - t0

            context.metrics["stage_times"][
                _stage_name(stage)
            ] = round(dt, 4)

            if debugger is not None:
                debugger.dump(stage, context)

        return context
