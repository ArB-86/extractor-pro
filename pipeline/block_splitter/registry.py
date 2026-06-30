from .splitters.heading import HeadingSplitter
from .splitters.section import SectionSplitter
from .splitters.exercise import ExerciseSplitter
from .splitters.example import ExampleSplitter
from .splitters.activity import ActivitySplitter
from .splitters.figure_it_out import FigureItOutSplitter
from .splitters.misc import MiscSplitter
from .splitters.sample_question import SampleQuestionSplitter
from .splitters.question import QuestionSplitter
from .splitters.paragraph import ParagraphSplitter


SPLITTERS = [
    HeadingSplitter,
    SectionSplitter,
    ExerciseSplitter,
    ExampleSplitter,
    ActivitySplitter,
    FigureItOutSplitter,
    MiscSplitter,
    SampleQuestionSplitter,
    QuestionSplitter,
    ParagraphSplitter,
]
