from __future__ import annotations

from src.question.v2.state import ParserState
from src.question.rules import RuleEngine


class ContextManager:

    def __init__(self):

        self.rules = RuleEngine()

        self.state = ParserState()

    def update(self, region):

        if region.page != self.state.page:

            self.state.page = region.page

            self.state.region_index = 0

        else:

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

            exercise = region.text.strip()

            if exercise != self.state.exercise:

                self.state.exercise = exercise

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

        
        self.state.metadata["last_block"] = block

        self.state.next_region()


        return self.state
