from __future__ import annotations

import re
from enum import Enum

from src.question.v2.context import StructuralPatterns
from src.question.v2.numbering import (
    NumberSignal,
    NumberingPatterns,
)
from src.question.v2.state import ParserState


class LineClass(str, Enum):
    QUESTION_START = "question_start"
    QUESTION_BODY = "question_body"
    OPTION = "option"
    SUBQUESTION = "subquestion"
    HEADER = "header"
    DROP = "drop"


_CAPTION = re.compile(r"^\s*(figure|fig\.?|table|chart|graph)\b", re.I)
_PAGE = re.compile(r"^\s*\d+\s*$")
_ALNUM = re.compile(r"[A-Za-z0-9]")
_CUE = re.compile(
    r"\b(find|solve|show|calculate|determine|prove|evaluate|write|state|define|what|which|why|how|construct|draw|verify|identify|simplify|factorise|expand)\b",
    re.I,
)


class BoundaryDetector:

    SUMMARY_HEADERS = (
        "summary",
        "chapter summary",
        "umm",
        "um m",
    )

    DROP_PREFIXES = (
        "ocr(",
        "page no",
        "page ",
        "figure it out",
        "figure it o1 ut",
        "figure it",
    )

    ANSWER_PREFIXES = (
        "ans.",
        "answer",
        "solution",
        "we get",
        "which is",
        "this is",
        "yes.",
        "yes,",
        "therefore",
        "hence",
        "for picture",
        "refer table",
        "refer figure",
    )

    EXPLANATION_PREFIXES = (
        "this is",
        "we get",
        "which is",
        "for picture",
        "refer",
        "yes,",
        "therefore",
        "hence",
        "thus",
    )

    GOOD_QUESTION_STARTS = {
        "what",
        "why",
        "which",
        "who",
        "where",
        "when",
        "how",

        "find",
        "draw",
        "write",
        "state",
        "show",
        "calculate",
        "determine",
        "prove",
        "construct",
        "identify",
        "observe",
        "complete",
        "fill",
        "choose",
        "match",

        # Added imperative verbs
        "count",
        "compare",
        "look",
        "measure",
        "estimate",
        "list",
        "arrange",
        "mark",
        "circle",
        "tick",
        "name",
        "explain",
        "discuss",
        "read",
        "make",
        "try",
        "check",

        "can",
        "is",
        "are",
        "do",
        "does",
    }

    def classify(
        self,
        *,
        text: str,
        state: ParserState,
        signal: NumberSignal,
    ) -> LineClass:

        # Normalize exactly like ContextManager
        text = text.strip()
        text = " ".join(text.split())
        lower = text.lower()

        if not text:
            return LineClass.DROP

        # Normalize for header detection
        normalized = re.sub(r"[^a-z0-9. ]", "", lower)

        # Early header detection
        if StructuralPatterns.SECTION.match(text):
            return LineClass.HEADER

        if StructuralPatterns.SECTION_LABEL.match(text):
            return LineClass.HEADER

        if normalized.replace(" ", "") == "summary":
            return LineClass.HEADER

        # Drop numbered answer lines
        if re.match(r"^\(?\d+\)?\s*ans", lower):
            print("DROP REASON: numbered answer")
            return LineClass.DROP

        # Drop OCR formulas with many '+' and few letters
        alpha = sum(c.isalpha() for c in text)
        if alpha < 8 and text.count("+") >= 2:
            print("DROP REASON: formula with many +")
            return LineClass.DROP

        # Age pattern
        if re.match(r"^[A-Za-z]\s*age\s+\d+", text, re.I):
            print("DROP REASON: age pattern")
            return LineClass.DROP

        if any(lower.startswith(x) for x in self.DROP_PREFIXES):
            print("DROP REASON: drop prefix")
            return LineClass.DROP

        if any(lower.startswith(x) for x in self.SUMMARY_HEADERS):
            return LineClass.HEADER

        if re.fullmatch(r"[qQ]\.?", text):
            print("DROP REASON: Q. alone")
            return LineClass.DROP

        if re.fullmatch(r"\d+", text):
            print("DROP REASON: standalone number")
            return LineClass.DROP

        if re.fullmatch(r"page\s*no\.?\s*\d+", lower):
            print("DROP REASON: page no")
            return LineClass.DROP

        if re.fullmatch(r"s\s*section\s*\d+.*", lower):
            return LineClass.HEADER

        if lower in {"section", "exercise", "chapter"}:
            return LineClass.HEADER

        if sum(c.isalpha() for c in text) < 5 and any(c.isdigit() for c in text):
            print("DROP REASON: too few alpha with digits")
            return LineClass.DROP

        print(
            f"[SUPPRESS] zone={state.zone} "
            f"signal={signal.kind} "
            f"text={text[:80]!r}"
        )

        if state.suppressed:
            return LineClass.DROP

        if _PAGE.match(text):
            print("DROP REASON: page")
            return LineClass.DROP

        if _CAPTION.match(text):
            print("DROP REASON: caption")
            return LineClass.DROP

        block = state.metadata.get("last_block")
        label = state.metadata.get("label")

        if block in ("chapter", "exercise"):
            return LineClass.HEADER

        if label == "title" and StructuralPatterns.SECTION.match(text):
            return LineClass.HEADER

        if label == "plain_text" and StructuralPatterns.SECTION_LABEL.match(text):
            return LineClass.HEADER

        if signal.kind == "option":
            return LineClass.OPTION if state.question_open else LineClass.DROP

        if signal.kind == "subquestion":
            return LineClass.SUBQUESTION if state.question_open else LineClass.DROP

        # ---------- QUESTION START HANDLING ----------
        if signal.kind == "question":
            remainder = NumberingPatterns.QUESTION_NUMBER.sub(
                "",
                text,
                count=1,
            ).strip()
            lower_rem = remainder.lower()

            # Drop answer-style patterns
            if re.match(r"^\d+(,\s*\d+)+", remainder):
                print("DROP REASON: number sequence as answer")
                return LineClass.DROP
            if "we get" in lower_rem and "?" not in remainder:
                print("DROP REASON: we get without ?")
                return LineClass.DROP
            if "for picture" in lower_rem:
                print("DROP REASON: for picture")
                return LineClass.DROP

            # Check if it's a valid question start
            first = remainder.split(maxsplit=1)[0].lower()
            print(
                "[QUESTION FILTER]",
                f"first={first!r}",
                f"text={remainder[:120]!r}",
            )
            if first not in self.GOOD_QUESTION_STARTS:
                print(f"DROP REASON: bad first word '{first}'")
                return LineClass.DROP

            if sum(c.isalpha() for c in remainder) < 5:
                print("DROP REASON: alpha<5")
                return LineClass.DROP

            if re.fullmatch(r"[,.\d ]+", remainder):
                print("DROP REASON: punctuation only")
                return LineClass.DROP

            if self._looks_like_heading(remainder):
                print("DROP REASON: looks like heading")
                return LineClass.HEADER

            return LineClass.QUESTION_START
        # ------------------------------------

        return LineClass.QUESTION_BODY if state.question_open else LineClass.DROP

    def _looks_like_heading(self, text: str) -> bool:
        lower = text.lower()

        if _CUE.search(text):
            return False

        if "?" in text:
            return False

        if "=" in text or "+" in text or "×" in text:
            return False

        if lower.startswith(("find", "solve", "draw", "write")):
            return False

        if len(text.split()) > 8:
            return False

        if text.endswith(":"):
            return True

        return (
            text == text.title()
            and not text.endswith("?")
        )
