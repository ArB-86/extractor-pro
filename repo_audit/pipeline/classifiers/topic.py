from __future__ import annotations


class TopicClassifier:

    KEYWORDS = {

        "polynomials": [
            "polynomial",
            "factor",
            "zero",
            "remainder",
            "quadratic",
            "cubic"
        ],

        "pair_of_linear_equations": [
            "linear equation",
            "pair of equations",
            "graphically",
            "solution of equations"
        ],

        "triangles": [
            "triangle",
            "pythagoras",
            "similar",
            "hypotenuse"
        ],

        "circles": [
            "circle",
            "sector",
            "segment",
            "arc",
            "radius",
            "diameter",
            "circumference"
        ],

        "coordinate_geometry": [
            "coordinate",
            "distance",
            "mid-point",
            "midpoint",
            "graph"
        ],

        "trigonometry": [
            "sin",
            "cos",
            "tan",
            "cot",
            "sec",
            "cosec"
        ],

        "probability": [
            "probability",
            "event",
            "dice",
            "coin",
            "card"
        ],

        "statistics": [
            "mean",
            "median",
            "mode",
            "histogram",
            "frequency"
        ]
    }

    def classify(self, question):

        text = question.question.lower()

        best = "general"
        score = 0

        for topic, words in self.KEYWORDS.items():

            hits = sum(
                1
                for w in words
                if w in text
            )

            if hits > score:
                score = hits
                best = topic

        return best
