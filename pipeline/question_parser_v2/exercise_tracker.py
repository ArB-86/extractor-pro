from __future__ import annotations

import re

from pipeline.layout.line import LayoutLine


_EXERCISE = re.compile(
    r"^(EXERCISE|Miscellaneous Exercise)\s*(.*)$",
    re.I,
)

_SECTION = re.compile(
    r"^\d+\.\d+"
)


class ExerciseTracker:

    def __init__(self):

        self.current_exercise = ""
        self.current_section = ""

    def update(self, line: LayoutLine):

        text = line.text.strip()

        m = _EXERCISE.match(text)

        if m:
            self.current_exercise = text
            return

        if _SECTION.match(text):
            self.current_section = text

    @property
    def exercise(self):
        return self.current_exercise

    @property
    def section(self):
        return self.current_section
