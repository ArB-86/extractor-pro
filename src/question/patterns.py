import re


CHAPTER_PATTERN = re.compile(
    r"^\s*chapter\s+(\d+)\s*[:.-]?\s*(.+)$",
    re.IGNORECASE,
)

EXERCISE_PATTERN = re.compile(
    r"^\s*exercise\s+(\d+(?:\.\d+)*)",
    re.IGNORECASE,
)

QUESTION_PATTERN = re.compile(
    r"^\s*(\d+)[.)]\s+(.+)$"
)

SUBQUESTION_PATTERN = re.compile(
    r"^\s*\(([a-z])\)\s+(.+)$",
    re.IGNORECASE,
)

MCQ_PATTERN = re.compile(
    r"^\s*\([A-D]\)",
    re.IGNORECASE,
)

TRUE_FALSE_PATTERN = re.compile(
    r"\b(true|false)\b",
    re.IGNORECASE,
)

ASSERTION_PATTERN = re.compile(
    r"assertion|reason",
    re.IGNORECASE,
)

FILL_PATTERN = re.compile(
    r"_{3,}"
)

CASE_STUDY_PATTERN = re.compile(
    r"case\s*study",
    re.IGNORECASE,
)

PROOF_PATTERN = re.compile(
    r"\bprove\b",
    re.IGNORECASE,
)

CONSTRUCTION_PATTERN = re.compile(
    r"\bconstruct\b",
    re.IGNORECASE,
)

HOTS_PATTERN = re.compile(
    r"\bhots\b|\bhigher order\b",
    re.IGNORECASE,
)

ACTIVITY_PATTERN = re.compile(
    r"\bactivity\b",
    re.IGNORECASE,
)

EXAMPLE_PATTERN = re.compile(
    r"\bexample\b",
    re.IGNORECASE,
)

FIGURE_PATTERN = re.compile(
    r"\bfig(?:ure)?\.?\s*\d+",
    re.IGNORECASE,
)

TABLE_PATTERN = re.compile(
    r"\btable\s*\d+",
    re.IGNORECASE,
)
