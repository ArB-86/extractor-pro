import re
from dataclasses import dataclass


@dataclass(slots=True)
class RuleResult:

    skip: bool = False

    block_type: str = "question"

    chapter: str | None = None

    exercise: str | None = None


class RuleEngine:

    # Only explicit "Chapter X" headings
    CHAPTER = re.compile(
        r"^\s*chapter\s+\d+\b",
        re.IGNORECASE,
    )

    EXERCISE = re.compile(
        r"^\s*(exercise|ex)\s+\d+(\.\d+)*",
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

    # New: explicit section heading
    SECTION = re.compile(
        r"^\s*section\s+\d+(?:\.\d+)+\b",
        re.IGNORECASE,
    )

    def analyze(self, text: str) -> RuleResult:

        t = text.strip()

        # Normalize before matching
        normalized = re.sub(r"\s+", " ", t)
        letters_only = re.sub(r"[^A-Za-z]", "", normalized).lower()
        compact = re.sub(r"[^A-Za-z0-9]", "", normalized).lower()

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

        # Summary detection
        if (
            self.SUMMARY.search(normalized)
            or "summary" in letters_only
            or letters_only.endswith("summary")
            or "summary" in compact
        ):
            return RuleResult(True, "summary")

        # OCR variants for summary
        if (
            letters_only in {
                "ummry",
                "ummary",
                "summaryy",
            }
            or letters_only.endswith("ummry")
        ):
            return RuleResult(True, "summary")

        if self.HISTORICAL.search(t):
            return RuleResult(True, "historical")

        # Expanded page header detection
        page_like = letters_only.lower()
        if (
            "pageno" in page_like
            or "page" in page_like
            or "ageno" in page_like
            or page_like.startswith("dage")
            or page_like.startswith("page")
        ):
            return RuleResult(True, "page")

        # ---- FIX: treat explicit "Section N" as section, not page ----
        if self.SECTION.match(t):
            return RuleResult(False, "section")

        return RuleResult(False, "question")
