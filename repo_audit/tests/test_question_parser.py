from __future__ import annotations

from dataclasses import dataclass

from pipeline.question_parser import QuestionParser


@dataclass
class Block:
    page: int
    text: str


@dataclass
class Section:
    title: str
    blocks: list[Block]


def parse_questions(block_texts: list[str]) -> list:
    section = Section(
        title="Exercise 1.1",
        blocks=[Block(1, text) for text in block_texts],
    )
    return QuestionParser(section).parse()


def test_stop_header_at_line_start_stops_capture() -> None:
    questions = parse_questions(
        [
            "1. Solve the problem carefully.",
            "Example 2:\nThis text should never be captured.",
            "2. This question must not be parsed.",
        ]
    )

    assert len(questions) == 1
    assert questions[0].question == "1. Solve the problem carefully."


def test_sentence_internal_heading_words_do_not_stop_capture() -> None:
    questions = parse_questions(
        [
            "1. In the following example, the word example appears inside a sentence.",
            "2. The next question should still be parsed.",
        ]
    )

    assert len(questions) == 2
    assert questions[0].question.startswith(
        "1. In the following example, the word example appears inside a sentence."
    )
    assert questions[1].question == "2. The next question should still be parsed."