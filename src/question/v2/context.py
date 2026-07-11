from __future__ import annotations

import re

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

        text = " ".join(
            (region.text or "").split()
        )

        result = self.rules.analyze(text)

        block = result.block_type

        if (
            region.label == "plain_text"
            and text.lower().startswith("section ")
        ):
            self.state.section = text
            return self.state

        if (
            region.label == "title"
            and text.lower().startswith("figure it out")
        ):
            self.state.inside_figure_it_out = True
            return self.state

        if (
            region.label == "title"
            and text.lower().startswith("summary")
        ):
            self.state.inside_summary = True
            return self.state

        # Updated chapter/section logic
        if block == "chapter":

            self.state.chapter = " ".join(text.split())
            self.state.reset_question()

        elif (
            region.label == "title"
            and re.match(r"^\d+\.\d+\s+[A-Za-z]", text)
        ):

            # FIX: This is a section, NOT a chapter
            self.state.section = text
            self.state.reset_question()

        elif block == "exercise":

            exercise = region.text.strip()

            if exercise != self.state.exercise:

                self.state.exercise = " ".join(
                    exercise.split()
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

        self.state.metadata["last_block"] = block

        self.state.next_region()

        return self.state
