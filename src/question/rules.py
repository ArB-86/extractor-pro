import re
from dataclasses import dataclass


@dataclass(slots=True)
class RuleResult:

    skip: bool = False

    block_type: str = "question"

    chapter: str | None = None

    exercise: str | None = None


class RuleEngine:

    CHAPTER = re.compile(
        r"^\s*chapter\s+\d+",
        re.IGNORECASE,
    )

    EXERCISE = re.compile(
        r"^\s*exercise\s+\d+(\.\d+)*",
        re.IGNORECASE,
    )

    EXAMPLE = re.compile(
        r"^\s*example\s+\d+(\.\d+)*",
        re.IGNORECASE,
    )

    ACTIVITY = re.compile(
        r"^\s*activity",
        re.IGNORECASE,
    )

    FIGURE_IT_OUT = re.compile(
        r"figure\s+it\s+out",
        re.IGNORECASE,
    )

    MISC = re.compile(
        r"miscellaneous\s+exercise",
        re.IGNORECASE,
    )

    SUMMARY = re.compile(
        r"summary",
        re.IGNORECASE,
    )

    HISTORICAL = re.compile(
        r"historical\s+note",
        re.IGNORECASE,
    )

    def analyze(self, text: str) -> RuleResult:

        t = text.strip()

        if self.CHAPTER.match(t):
            return RuleResult(False, "chapter")

        if self.EXERCISE.match(t):
            return RuleResult(False, "exercise")

        if self.EXAMPLE.match(t):
            return RuleResult(False, "example")

        if self.ACTIVITY.match(t):
            return RuleResult(False, "activity")

        if self.FIGURE_IT_OUT.search(t):
            return RuleResult(False, "figure_it_out")

        if self.MISC.search(t):
            return RuleResult(False, "misc")

        if self.SUMMARY.search(t):
            return RuleResult(True, "summary")

        if self.HISTORICAL.search(t):
            return RuleResult(True, "historical")

        return RuleResult(False, "question")
