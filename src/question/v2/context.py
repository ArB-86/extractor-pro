from __future__ import annotations

from src.question.v2.state import ParserState
from src.question.rules import RuleEngine


class ContextManager:

    def __init__(self):

        self.rules = RuleEngine()

        self.state = ParserState()

    def update(self, region):

        self.state.page = region.page

        result = self.rules.analyze(
            region.text or ""
        )

        block = result.block_type

        if block == "chapter":

            self.state.chapter = (
                region.text.strip()
            )

            self.state.reset_question()

        elif block == "exercise":

            self.state.exercise = (
                region.text.strip()
            )

            self.state.reset_question()

        self.state.inside_example = (
            block == "example"
        )

        self.state.inside_activity = (
            block == "activity"
        )

        self.state.inside_miscellaneous = (
            block == "misc"
        )

        self.state.inside_figure_it_out = (
            block == "figure_it_out"
        )

        self.state.inside_summary = (
            block == "summary"
        )

        self.state.next_region()

        return self.state
