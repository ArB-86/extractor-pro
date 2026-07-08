
from pipeline.core.context import PipelineContext
from pipeline.core.engine import PipelineEngine
from pipeline.core.registry import Registry
from pipeline.core.question_enrichment_stage import QuestionEnrichmentStage

ctx = PipelineContext()

ctx.questions = []

r = Registry()

r.register(
    QuestionEnrichmentStage()
)

ctx = PipelineEngine(
    r.build()
).run(ctx)

print(ctx.metrics)
print("OK")
