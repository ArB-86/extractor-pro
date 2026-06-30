from __future__ import annotations

import re

from models.question import Question


QUESTION_START = re.compile(
    r"^\s*\*?\s*([1-9][0-9]*)\.(?:\s|\n|$)"
)


def _is_real_question_start(text: str) -> bool:

    m = QUESTION_START.match(text)

    if not m:
        return False

    lines = [x.strip() for x in text.splitlines() if x.strip()]

    if len(lines) == 1:
        return True

    second = lines[1]

    # Table rows
    if len(second.split()) <= 2:
        return False

    # Gender column
    if second in {"M", "F"}:
        return False

    # Pure numbers
    if second.replace(".", "").isdigit():
        return False

    return True


_QUESTION_STOP = re.compile(
    r"^(?:"
    r"Sample Question\s*\d*"
    r"|Solution\s*:?"
    r"|Hints?\s+to\s+Selected\s+Problems"
    r"|Determine whether each of the statement in Exercises"
    r"|Choose the correct answers from the given four options"
    r"|Fill in the blanks in each of the Exercises"
    r"|State True or False for the following statements"
    r")",
    re.I,
)

_STOP_LINE_PATTERNS = (
    _QUESTION_STOP,
    re.compile(r"^\([D-E]\)\s*(?:Activities|Activity)", re.I),
    re.compile(r"^\(D\)\s*Short\s+Answer", re.I),
    re.compile(r"^\(E\)\s*Long\s+Answer", re.I),

    # Safe textbook boundaries
    re.compile(r"^Example(?:\s+\d+)?\b", re.I),
    re.compile(r"^Try\s+This\b", re.I),
    re.compile(r"^Reprint\b", re.I),
    re.compile(r"^Summary\b", re.I),
    re.compile(r"^Exercise(?:\s+\d+(?:\.\d+)?)?\b", re.I),
    re.compile(r"^Activity(?:\s+\d+)?\b", re.I),
    re.compile(r"^Figure(?:\s+it\s+Out|\s+It\s+Out|\s+It\s+out)?\b", re.I),

    re.compile(r"^Try$", re.I),
    re.compile(r"^This$", re.I),

    re.compile(r"^Math$", re.I),
    re.compile(r"^Talk$", re.I),

    re.compile(r"^Miscellaneous\s+Examples\b", re.I),
    re.compile(r"^Miscellaneous\s+Exercise\b", re.I),
    re.compile(r"^Historical\s+Note\b", re.I),
)


def _normalize_key(text: str) -> str:
    return " ".join(text.split()).strip().lower()


def _has_stop_header(text: str) -> bool:
    lines = text.splitlines()

    for line in lines:

        stripped = line.strip()

        if not stripped:
            continue

        # Don't treat a question number as a stop header.
        if QUESTION_START.match(stripped):
            continue

        if any(pattern.match(stripped) for pattern in _STOP_LINE_PATTERNS):
            return True

    return False


class QuestionParser:

    def __init__(self, section, source: str = "NCERT", chapter: str = ""):

        self.section = section
        self.source = source
        self.chapter = chapter

    def parse(self):

        questions: list[Question] = []
        current: Question | None = None
        seen_ids: set[int] = set()
        seen_text: set[str] = set()

        for block in self.section.blocks:

            text = block.text.strip()

            if not text:
                continue

            # Detect section breaks inside oversized questions
            if (
                current is not None
                and not QUESTION_START.match(text)
                and len(text.splitlines()) >= 2
            ):
                first = text.splitlines()[0].strip()

                if (
                    first
                    and first[0].isupper()
                    and not first.endswith("?")
                    and not first.endswith(":")
                    and len(first.split()) >= 4
                ):
                    questions.append(current)
                    current = None
                    continue

            lines = text.splitlines()

            stop_idx = None

            for i, line in enumerate(lines):

                s = line.strip()

                for p in _STOP_LINE_PATTERNS:
                    if p.match(s):
                        print("=" * 80)
                        print("STOP MATCH")
                        print("SECTION:", self.section.title)
                        print("LINE:", repr(s))
                        print("PATTERN:", p.pattern)
                        stop_idx = i
                        break

                if stop_idx is not None:
                    break

            if stop_idx is not None:

                if current is not None and stop_idx > 0:
                    before = "\n".join(lines[:stop_idx]).strip()

                    if before:
                        current.question += "\n" + before

                    current.page_end = block.page

                    questions.append(current)
                    current = None

                continue

            m = QUESTION_START.match(text) if _is_real_question_start(text) else None

            if m:

                qid = int(m.group(1))

                if qid in seen_ids:
                    if current is not None:
                        questions.append(current)
                        current = None
                    continue

                if current is not None:
                    questions.append(current)

                seen_ids.add(qid)
                current = Question(
                    id=qid,
                    source=self.source,
                    chapter=self.chapter,
                    exercise=self.section.title,
                    page_start=block.page,
                    page_end=block.page,
                    question_type="",
                    question=text,
                )
                continue

            if current is not None:

                if text.strip() == "Exploring Some Geometric Themes":
                    continue

                if text.startswith("Ganita Prakash |"):
                    continue

                if text.strip().startswith("Miscellaneous Examples"):
                    questions.append(current)
                    current = None
                    continue

                if text.strip().startswith("Historical Note"):
                    questions.append(current)
                    current = None
                    continue

                if text.strip().startswith("Summary"):
                    questions.append(current)
                    current = None
                    continue

                key = _normalize_key(text)
                if key and key in seen_text:
                    continue

                if key:
                    seen_text.add(key)

                current.question += "\n" + text
                current.page_end = block.page

        if current is not None:
            questions.append(current)

        return questions