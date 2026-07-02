from dataclasses import dataclass, field

@dataclass(slots=True)
class DocumentNode:
    title: str = ""
    children: list = field(default_factory=list)

@dataclass(slots=True)
class ChapterNode(DocumentNode):
    number: str = ""

@dataclass(slots=True)
class SectionNode(DocumentNode):
    number: str = ""

@dataclass(slots=True)
class ExerciseNode(DocumentNode):
    number: str = ""

@dataclass(slots=True)
class ExampleNode(DocumentNode):
    number: str = ""

@dataclass(slots=True)
class QuestionNode(DocumentNode):
    question_no: str = ""
    text: str = ""
    page: int = 0

@dataclass(slots=True)
class FormulaNode(DocumentNode):
    latex: str = ""

@dataclass(slots=True)
class FigureNode(DocumentNode):
    caption: str = ""

@dataclass(slots=True)
class TableNode(DocumentNode):
    caption: str = ""
