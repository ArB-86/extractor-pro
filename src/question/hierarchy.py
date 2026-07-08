from src.question.context import ExtractionContext
from src.question.rules import RuleEngine


class HierarchyBuilder:

    def __init__(self):

        self.rules = RuleEngine()

        self.context = ExtractionContext()

    def process(self, region):

        if not region.text:
            return self.context

        result = self.rules.analyze(
            region.text
        )

        self.context.page = region.page

        self.context.update(result)

        return self.context
