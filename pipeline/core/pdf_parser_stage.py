from pipeline.core.stage import Stage
from parsers.pdf_parser import PDFParser

class PDFParserStage(Stage):

    def run(self, context):

        context.blocks = PDFParser(context.pdf).extract()

        return context
