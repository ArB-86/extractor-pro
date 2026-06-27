
from pipeline.core.registry import Registry

from pipeline.core.pdf_parser_stage import PDFParserStage
from pipeline.core.block_splitter_stage import BlockSplitterStage
from pipeline.core.block_merger_stage import BlockMergerStage
from pipeline.core.layout_cleaner_stage import LayoutCleanerStage
from pipeline.core.section_parser_stage import SectionParserStage
from pipeline.core.question_parser_stage import QuestionParserStage
from pipeline.core.question_enrichment_stage import QuestionEnrichmentStage
from pipeline.core.metrics_stage import MetricsStage


def build():

    r = Registry()

    r.register(PDFParserStage())
    r.register(BlockSplitterStage())
    r.register(BlockMergerStage())
    r.register(LayoutCleanerStage())
    r.register(SectionParserStage())
    r.register(QuestionParserStage())
    r.register(QuestionEnrichmentStage())
    r.register(MetricsStage())

    return r.build()
