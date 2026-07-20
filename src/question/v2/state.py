from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class SuppressionZone(str, Enum):

    NONE = "none"

    EXAMPLE = "example"

    ACTIVITY = "activity"

    MISCELLANEOUS = "misc"

    FIGURE_IT_OUT = "figure_it_out"

    SUMMARY = "summary"

    HISTORICAL = "historical"

    ANSWER = "answer"


@dataclass(slots=True)
class ParserState:

    chapter: str | None = None

    chapter_number: int | None = None

    exercise: str | None = None

    section: str | None = None

    page: int = 0

    region_index: int = 0

    question_number: str | None = None

    subquestion: str | None = None

    question_open: bool = False

    zone: SuppressionZone = SuppressionZone.NONE

    metadata: dict = field(default_factory=dict)

    @property
    def suppressed(self):

        return self.zone is not SuppressionZone.NONE

    @property
    def inside_example(self):

        return self.zone is SuppressionZone.EXAMPLE

    @property
    def inside_activity(self):

        return self.zone is SuppressionZone.ACTIVITY

    @property
    def inside_miscellaneous(self):

        return self.zone is SuppressionZone.MISCELLANEOUS

    @property
    def inside_figure_it_out(self):

        return self.zone is SuppressionZone.FIGURE_IT_OUT

    @property
    def inside_summary(self):

        return self.zone is SuppressionZone.SUMMARY

    @property
    def inside_solution(self):

        return self.zone is SuppressionZone.ANSWER

    @property
    def inside_answer(self):

        return self.zone is SuppressionZone.ANSWER

    def enter_zone(
        self,
        zone: SuppressionZone,
    ):

        self.zone = zone

    def exit_zone(self):

        self.zone = SuppressionZone.NONE

    def reset_question(self):

        self.question_number = None

        self.subquestion = None

        self.question_open = False

    def next_region(self):

        self.region_index += 1
