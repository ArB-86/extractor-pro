from pathlib import Path

from pipeline.core.context import PipelineContext
from pipeline.core.default_pipeline import build
from pipeline.core.engine import PipelineEngine


PDF = Path(
    "/home/jiitcah.05/nlp_research_module/datasets/raw_docs/kemh1dd/kemh106.pdf"
)

context = PipelineContext(pdf=str(PDF))

PipelineEngine(build()).run(
    context,
    debug_dir="debug",
)

print("=" * 60)
print("Blocks:", len(context.blocks))
print("Questions:", len(context.questions))
print("=" * 60)
