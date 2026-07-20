from __future__ import annotations

import re

from src.question.rules import RuleEngine
from src.question.v2.state import ParserState, SuppressionZone
from src.question.v2.heading_classifier import HeadingClassifier, HeadingType
from src.question.v2.heading_normalizer import HeadingNormalizer


class StructuralPatterns:

    # Stricter SECTION regex: prevents garbage like 3.367813.13 二
    SECTION = re.compile(
        r"""
        ^
        \s*
        (?:
            (?P<prefix>[A-Za-z][A-Za-z ]+?)\s+
        )?
        (?P<num>\d{1,2}(?:\.\d{1,2})*)
        \s+
        (?P<title>[A-Za-z][A-Za-z0-9(),:;'\- ]{3,})
        $
        """,
        re.X,
    )

    SECTION_LABEL = re.compile(
        r"^\s*section\s+\S",
        re.I,
    )

    ANSWER_HEADER = re.compile(
        r"^\s*(answers?|solutions?|hints?|summary)\b",
        re.I,
    )


_ZONE_BLOCKS = {
    "example": SuppressionZone.EXAMPLE,
    "activity": SuppressionZone.ACTIVITY,
    "misc": SuppressionZone.MISCELLANEOUS,
    "figure_it_out": SuppressionZone.FIGURE_IT_OUT,
    "summary": SuppressionZone.SUMMARY,
    "historical": SuppressionZone.HISTORICAL,
}


class ContextManager:

    def __init__(self):

        self.rules = RuleEngine()
        self.state = ParserState()

        self.heading_classifier = HeadingClassifier()
        self.heading_normalizer = HeadingNormalizer()

    def update(self, region):

        state = self.state

        if region.page != state.page:

            print(f"[CONTEXT] Page changed: {state.page} -> {region.page}")
            state.page = region.page
            state.metadata["page"] = region.page

            # Reset transient structural context on every new page
            state.exit_zone()
            state.reset_question()
            state.section = None

        text = " ".join(
            (region.text or "").split()
        )

        # ---- Heading classification and normalization for title regions ----
        if region.label == "title":

            kind = self.heading_classifier.classify(text)

            if kind in {
                HeadingType.TABLE,
                HeadingType.FIGURE,
                HeadingType.SUMMARY,
                HeadingType.PAGE,
                HeadingType.UNKNOWN,
            }:
                state.metadata["text"] = text
                state.metadata["label"] = region.label
                state.metadata["last_block"] = "ignored"
                state.metadata["source_type"] = "ignored"
                state.next_region()
                return state

            # Normalize the heading (e.g., fix 1.61 → 1.6)
            text = self.heading_normalizer.normalize(text)

        # ---- Kill Summary pages (even if not a title) ----
        compact = re.sub(r"[^a-z0-9]", "", text.lower())

        if compact in {
            "summary",
            "umm2ry",
            "ummary",
            "summaryquestions",
        }:
            state.enter_zone(SuppressionZone.SUMMARY)
            state.metadata["text"] = text
            state.metadata["label"] = region.label
            state.metadata["last_block"] = "summary"
            state.metadata["source_type"] = "recap"
            state.next_region()
            return state

        # Fix OCR spacing in section numbers (global, not just titles)
        text = re.sub(
            r"(?<=\d)\s+(?=\d)",
            ".",
            text,
        )
        text = re.sub(
            r"\.{2,}",
            ".",
            text,
        )

        label = region.label

        result = self.rules.analyze(text)

        block = result.block_type

        # Handle page headers from RuleEngine
        if block == "page":
            state.metadata["text"] = text
            state.metadata["label"] = label
            state.metadata["last_block"] = block
            state.metadata["source_type"] = "header"
            state.next_region()
            return state

        state.metadata["text"] = text
        state.metadata["label"] = label
        state.metadata["last_block"] = block

        # ---- Default source_type ----
        state.metadata["source_type"] = "textbook"

        # ---- Set source_type based on zone/block ----
        if state.zone is SuppressionZone.SUMMARY:
            state.metadata["source_type"] = "recap"

        elif block == "figure_it_out":
            state.metadata["source_type"] = "figure_it_out"

        elif block == "activity":
            state.metadata["source_type"] = "activity"

        elif block == "example":
            state.metadata["source_type"] = "example"

        elif block == "exercise":
            state.metadata["source_type"] = "exercise"

        if block == "chapter":

            # ---- Guard: reject OCR garbage chapter titles ----
            if (
                sum(c.isalpha() for c in text) < 5
                or re.fullmatch(r"[\d\s.,:;()\-_=+/*\\]+", text)
            ):
                state.metadata["text"] = text
                state.metadata["label"] = label
                state.metadata["last_block"] = block
                state.next_region()
                return state

            state.chapter = text

            state.chapter_number = self._chapter_number(text)

            state.exercise = None

            state.section = None

            state.reset_question()

            state.exit_zone()

        elif block == "exercise":

            state.exercise = text

            state.reset_question()

            state.exit_zone()

        # ----- SECTION DETECTION with stricter regex -----
        elif (
            StructuralPatterns.SECTION.match(text)
            or StructuralPatterns.SECTION_LABEL.match(text)
        ):

            m = StructuralPatterns.SECTION.match(text)

            if m:

                number = m.group("num")
                title = " ".join(
                    m.group("title").split()
                )
                prefix = m.groupdict().get("prefix")

                state.section = number
                if prefix:
                    state.chapter = f"{prefix} {number} {title}"
                else:
                    state.chapter = f"{number} {title}"

                state.metadata["section"] = number
                state.metadata["section_title"] = title
                state.metadata["section_prefix"] = prefix

            state.reset_question()
            state.exit_zone()

        # zone handling
        zone = _ZONE_BLOCKS.get(block)

        if zone is SuppressionZone.FIGURE_IT_OUT:
            state.exit_zone()
        elif zone is not None:
            state.enter_zone(zone)

        elif StructuralPatterns.ANSWER_HEADER.match(text):
            state.enter_zone(
                SuppressionZone.ANSWER
            )

        # ---- Record the y-coordinate of this region for future flow checks ----
        state.metadata["last_y"] = region.y1

        state.next_region()

        return state

    @staticmethod
    def _chapter_number(text):
        m = re.search(
            r"\d+(?:\.\d+)?",
            text,
        )
        if m:
            return m.group()
        return None
