
from dataclasses import dataclass, field


@dataclass
class PipelineContext:

    pdf: str = ""

    blocks: list = field(default_factory=list)

    questions: list = field(default_factory=list)

    figures: list = field(default_factory=list)

    tables: list = field(default_factory=list)

    metadata: dict = field(default_factory=dict)

    metrics: dict = field(default_factory=dict)

    errors: list = field(default_factory=list)
