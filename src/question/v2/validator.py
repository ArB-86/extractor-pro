from __future__ import annotations

import re

from src.question.models import QuestionCandidate


class QuestionValidator:

    HEADER_PATTERNS = (
        "mathematics",
        "ncert",
        "chapter",
        "exercise",
        "page",
    )

    OCR_FIXES = {
        "ﬁ":"fi",
        "ﬂ":"fl",
        "—":"-",
        "–":"-",
        "“":'"',
        "”":'"',
        "‘":"'",
        "’":"'",
        "\u00a0":" ",
    }


    MIN_WORDS = 3

    MAX_WORDS = 1200

    INVALID_START = (
        "chapter",
        "exercise",
        "summary",
        "contents",
        "index",
    )

    PAGE_ONLY = re.compile(r"^\d+$")


    def confidence(self, text):

        score = 1.0

        words = len(text.split())

        if words < 5:
            score -= 0.35

        if words > 250:
            score -= 0.15

        if text.count("?") > 1:
            score -= 0.10

        if text.count("\n") > 25:
            score -= 0.15

        if re.search(r"[|]{2,}", text):
            score -= 0.15

        return max(0.0, min(1.0, score))


    def validate(
        self,
        questions: list[QuestionCandidate],
    ) -> list[QuestionCandidate]:

        valid = []

        for q in questions:

            text = q.text

            for a,b in self.OCR_FIXES.items():
                text = text.replace(a,b)

            text = re.sub(
                r"[ \t]+",
                " ",
                text,
            )

            text = re.sub(
                r"\n{3,}",
                "\n\n",
                text,
            )

            text = re.sub(
                r"([a-z,])\n([a-z])",
                r"\1 \2",
                text,
            )

            text = re.sub(
                r"(\w)-\n(\w)",
                r"\1\2",
                text,
            ).strip()

            text = re.sub(
                r"(\b\d+[.)])\s+\1",
                r"\1",
                text,
            )

            if not text:
                continue

            if self.PAGE_ONLY.fullmatch(text):
                continue

            if len(text.split()) < self.MIN_WORDS:
                continue

            if len(text.split()) > self.MAX_WORDS:
                continue

            if text.lower().startswith(self.INVALID_START):
                continue

            if any(
                text.lower().startswith(x)
                for x in self.HEADER_PATTERNS
            ):
                continue

            alpha = sum(c.isalpha() for c in text)

            if alpha < 3:
                continue

            if re.fullmatch(r"[\W\d_ ]+", text):
                continue

            if len(text) < 12:
                continue

            lines = []

            seen = set()

            option_seen = set()

            for line in text.split("\n"):

                key = line.strip()

                if not key:
                    continue

                if re.match(
                    r"^\([A-D]\)",
                    key,
                    re.I,
                ):

                    tag = key[:3].upper()

                    if tag in option_seen:
                        continue

                    option_seen.add(tag)

                if key in seen:
                    continue

                seen.add(key)

                lines.append(key)

            q.text = "\n".join(lines)

            q.confidence = self.confidence(
                q.text,
            )

            valid.append(q)

        return valid
