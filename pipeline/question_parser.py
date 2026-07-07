from __future__ import annotations
import re
from typing import List, Any
from pipeline.models.question import Question

class QuestionParser:
    def __init__(self, data: Any, source: str = "NCERT", chapter: str = ""):
        self.paragraphs = getattr(data, 'blocks', getattr(data, 'paragraphs', getattr(data, 'children', [])))
        self.source = source
        self.chapter = chapter
        # Smarter Regex: Catches '1.', '1)', 'Q1.'
        self.pattern = re.compile(r"(?m)^[\s*]*(?:Q|q)?(\d+)[\.\)]\s+")

    def parse(self) -> List[Question]:
        questions, qid, current = [], 1, None
        for para in self.paragraphs:
            text = getattr(para, 'text', '').strip()
            if not text or len(text) < 15: continue
            
            if self.pattern.match(text):
                if current: questions.append(current)
                current = Question(
                    question_id=qid,
                    source=self.source,
                    chapter=self.chapter,
                    page_start=getattr(para, "page", 0),
                    page_end=getattr(para, "page", 0),
                    question=text,
                )
                qid += 1
            elif current:
                current.question += " " + text
                current.page_end = getattr(para, "page", current.page_end)  # update page if moving forward
        if current: questions.append(current)
        return questions