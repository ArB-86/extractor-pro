from __future__ import annotations

from collections import Counter

from pipeline.layout.line import LayoutLine


class MarginDetector:

    def detect(self, lines: list[LayoutLine]) -> float:

        candidates = []

        for line in lines:

            text = line.text.strip()

            if not text:
                continue

            # Ignore centered/short formula fragments
            if len(text) < 8:
                continue

            # Ignore equation-heavy lines
            if (
                "=" in text
                or "×" in text
                or "÷" in text
                or "√" in text
            ):
                continue

            # Ignore figure captions
            if text.startswith(("Fig", "Figure")):
                continue

            candidates.append(round(line.indent))

        if not candidates:
            candidates = [round(l.indent) for l in lines]

        return float(Counter(candidates).most_common(1)[0][0])
