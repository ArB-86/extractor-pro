from __future__ import annotations

import re

QUESTION_START = re.compile(
    r"(?m)^(?P<star>\*)?(?P<number>\d+)\.\s+"
)

SUBQUESTION_ALPHA = re.compile(
    r"(?m)^\([a-z]\)\s+"
)

SUBQUESTION_ROMAN = re.compile(
    r"(?m)^\((?:i|ii|iii|iv|v|vi|vii|viii|ix|x)\)\s+"
)

EXERCISE = re.compile(
    r"(?i)^Exercise(?:\s+Set)?\s+\d+(?:\.\d+)?"
)

EXAMPLE = re.compile(
    r"(?i)^Example\s+\d+(?:\.\d+)?"
)

ACTIVITY = re.compile(
    r"(?i)^Activity\b"
)

FIGURE_IT_OUT = re.compile(
    r"(?i)^Figure\s+it\s+Out"
)

MISC_EXERCISE = re.compile(
    r"(?i)^Miscellaneous\s+Exercise"
)

SAMPLE_QUESTION = re.compile(
    r"(?i)^Sample\s+Questions?"
)
