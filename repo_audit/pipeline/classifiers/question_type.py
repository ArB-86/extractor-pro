from __future__ import annotations

import re


class QuestionTypeClassifier:

    def classify(self, question):

        text = question.question.lower()

        # -------------------------
        # MCQ
        # -------------------------

        if question.options:
            return "mcq"

        # -------------------------
        # True / False
        # -------------------------

        if (
            "true or false" in text
            or "true/false" in text
            or "is it true" in text
            or "justify whether" in text
        ):
            return "true_false"

        # -------------------------
        # Assertion Reason
        # -------------------------

        if (
            "assertion" in text
            and "reason" in text
        ):
            return "assertion_reason"

        # -------------------------
        # Fill blanks
        # -------------------------

        if (
            "fill in the blanks" in text
            or "fill in the blank" in text
            or "________" in text
            or "____" in text
        ):
            return "fill_blank"

        # -------------------------
        # Match the following
        # -------------------------

        if (
            "match the following" in text
            or "match following" in text
        ):
            return "match"

        # -------------------------
        # Proof
        # -------------------------

        if (
            "prove that" in text
            or "show that" in text
        ):
            return "proof"

        # -------------------------
        # Construction
        # -------------------------

        if (
            "construct" in text
            or "construction" in text
        ):
            return "construction"

        # -------------------------
        # Graph
        # -------------------------

        if (
            "draw the graph" in text
            or "graphically" in text
            or "plot" in text
        ):
            return "graph"

        # -------------------------
        # Numerical
        # -------------------------

        if (
            "find" in text
            or "calculate" in text
            or "determine" in text
            or "evaluate" in text
            or "solve" in text
        ):
            return "numerical"

        # -------------------------
        # Default
        # -------------------------

        return "descriptive"
