from __future__ import annotations

from dataclasses import dataclass, field


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

    inside_example: bool = False

    inside_activity: bool = False

    inside_miscellaneous: bool = False

    inside_figure_it_out: bool = False

    inside_summary: bool = False

    inside_solution: bool = False

    inside_answer: bool = False

    metadata: dict = field(default_factory=dict)

    def reset_question(self):

        self.question_number = None

        self.subquestion = None

        self.inside_solution = False

        self.inside_answer = False

    def next_region(self):

        self.region_index += 1
