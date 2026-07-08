from pipeline.core.registry import Registry

from pipeline.core.metadata_stage import DocumentGateStage, MetadataStage
from pipeline.core.pdf_parser_stage import PDFParserStage
from pipeline.core.block_splitter_stage import BlockSplitterStage
from pipeline.core.block_merger_stage import BlockMergerStage
from pipeline.core.block_normalizer_stage import BlockNormalizerStage
from pipeline.core.layout_cleaner_stage import LayoutCleanerStage
from pipeline.core.section_parser_stage import SectionParserStage
from pipeline.core.question_parser_v3_stage import QuestionParserV3Stage
from pipeline.core.question_enrichment_stage import QuestionEnrichmentStage
from pipeline.core.metrics_stage import MetricsStage
from pipeline.core.export_stage import ExportStage

def build():
    r = Registry()

    r.register(MetadataStage())
    r.register(PDFParserStage())
    r.register(DocumentGateStage())
    r.register(BlockSplitterStage())
    r.register(BlockMergerStage())
    r.register(BlockNormalizerStage())
    r.register(LayoutCleanerStage())
    r.register(SectionParserStage())
    r.register(QuestionParserV3Stage())
    r.register(QuestionEnrichmentStage())
    r.register(MetricsStage())
    # Register the exporter with a target file path
    r.register(ExportStage("output/json/final_dataset.json"))

    return r.build()
