from __future__ import annotations

import re


class HeadingNormalizer:

    @staticmethod
    def normalize(text: str) -> str:

        text = " ".join(text.split())

        text = re.sub(
            r"(?<=\d)\s+(?=\d)",
            ".",
            text,
        )

        m = re.match(
            r"""
            ^
            (?P<prefix>[A-Za-z ]+?)?
            \s*
            (?P<num>\d+\.\d\d)
            \s+
            (?P<title>.+)
            $
            """,
            text,
            re.X,
        )

        if m:

            num = m.group("num")

            major, minor = num.split(".")

            if len(minor) == 2 and minor.endswith("1"):

                minor = minor[:-1]

                num = f"{major}.{minor}"

                prefix = m.group("prefix") or ""

                return f"{prefix} {num} {m.group('title')}".strip()

        return text
