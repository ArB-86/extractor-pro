from dataclasses import dataclass, field
from typing import Optional, Dict, Any

@dataclass
class Question:
    id: int
    source: str
    chapter: str
    page_start: int
    page_end: int
    exercise: str = ""
    question_type: str = "unknown"
    question: str = ""
    options: Optional[Dict[str, str]] = field(default_factory=dict)
    answer: str = ""
    solution: str = ""
    difficulty: str = "medium"
    topic: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
