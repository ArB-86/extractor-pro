from models.question import Question
from pipeline.classifiers.question_type import QuestionTypeClassifier

classifier = QuestionTypeClassifier()

samples = [

    Question(
        id=1,
        source="test",
        chapter="1",
        exercise="EXERCISE",
        page_start=1,
        page_end=1,
        question_type="unknown",
        question="Find the value of x."
    ),

    Question(
        id=2,
        source="test",
        chapter="1",
        exercise="EXERCISE",
        page_start=1,
        page_end=1,
        question_type="unknown",
        question="Show that tan²A + 1 = sec²A."
    ),

    Question(
        id=3,
        source="test",
        chapter="1",
        exercise="EXERCISE",
        page_start=1,
        page_end=1,
        question_type="unknown",
        question="Is it true that x+y=5?"
    ),

    Question(
        id=4,
        source="test",
        chapter="1",
        exercise="EXERCISE",
        page_start=1,
        page_end=1,
        question_type="unknown",
        question="Draw the graph of y=x."
    ),

    Question(
        id=5,
        source="test",
        chapter="1",
        exercise="EXERCISE",
        page_start=1,
        page_end=1,
        question_type="unknown",
        question="Construct a triangle."
    ),

    Question(
        id=6,
        source="test",
        chapter="1",
        exercise="EXERCISE",
        page_start=1,
        page_end=1,
        question_type="unknown",
        question="Fill in the blanks."
    ),

    Question(
        id=7,
        source="test",
        chapter="1",
        exercise="EXERCISE",
        page_start=1,
        page_end=1,
        question_type="unknown",
        question="Choose the correct answer.",
        options={
            "A": "1",
            "B": "2"
        }
    ),

]

for q in samples:
    print(f"{q.question} -> {classifier.classify(q)}")