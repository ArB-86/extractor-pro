from pipeline.models import Paragraph
from pipeline.block_splitter.splitters.question import QuestionSplitter


def test_multiple_questions():

    block = Paragraph(
        page=1,
        bbox=(0, 0, 0, 0),
        text="""
2. Toss a coin twice.

Find the probability.

3. Throw a die.

Find the probability.
""",
    )

    result = QuestionSplitter().split([block])

    assert len(result) == 2
    assert result[0].metadata["question_no"] == "2"
    assert result[1].metadata["question_no"] == "3"
