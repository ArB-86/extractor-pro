
from pipeline.core.context import PipelineContext
from pipeline.core.report import PipelineReport

ctx = PipelineContext()

ctx.metrics = {

"stage_times":{

"A":0.12,

"B":0.43

}

}

ctx.questions=[1,2,3]

ctx.figures=[1]

PipelineReport().print(ctx)
