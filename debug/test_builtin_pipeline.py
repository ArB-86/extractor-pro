
from pipeline.core.context import PipelineContext
from pipeline.core.engine import PipelineEngine
from pipeline.core.registry import Registry

from pipeline.core.builtin_stages import (
    EnrichmentStage,
    ValidationStage,
    AIStage
)

ctx = PipelineContext()

r = Registry()

r.register(EnrichmentStage())
r.register(ValidationStage())
r.register(AIStage())

engine = PipelineEngine(r.build())

ctx = engine.run(ctx)

print(type(ctx).__name__)
print("Pipeline OK")
