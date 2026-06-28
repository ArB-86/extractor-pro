from __future__ import annotations

import re

from models.question import Question


QUESTION_START = re.compile(r"^\s*([1-9][0-9]*)\.(?:\s|\n|$)")

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
    re.compile(r"^Example(?:\s+\d+)?\b", re.I),
    re.compile(r"^Try\s+This\b", re.I),
    re.compile(r"^Reprint\b", re.I),
    re.compile(r"^Summary\b", re.I),
    re.compile(r"^Exercise(?:\s+\d+(?:\.\d+)?)?\b", re.I),
    re.compile(r"^Activity(?:\s+\d+)?\b", re.I),
    re.compile(r"^Figure(?:\s+it\s+Out|\s+It\s+Out|\s+It\s+out)?\b", re.I),
)


def _normalize_key(text: str) -> str:
    return " ".join(text.split()).strip().lower()


def _has_stop_header(text: str) -> bool:
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
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

            if _has_stop_header(text):
                break

            m = QUESTION_START.match(text)

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
