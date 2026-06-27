from __future__ import annotations


class DifficultyClassifier:

    def classify(self, question):

        text = question.question.lower()

        score = 0

        # Long questions
        if len(text) > 250:
            score += 2
        elif len(text) > 120:
            score += 1

        # Proofs
        if (
            "prove" in text
            or "show that" in text
        ):
            score += 2

        # Graphs
        if (
            "graph" in text
            or "draw" in text
            or "construct" in text
        ):
            score += 1

        # Multiple calculations
        if (
            "hence" in text
            or "therefore" in text
            or "justify" in text
            or "derive" in text
        ):
            score += 1

        # MCQs are usually easier
        if question.options:
            score -= 1

        if score <= 0:
            return "easy"

        if score <= 2:
            return "medium"

        return "hard"
