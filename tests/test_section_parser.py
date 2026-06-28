from __future__ import annotations

from dataclasses import dataclass

import pytest

from pipeline.section_parser import SectionParser


@dataclass
class Block:
    page: int
    text: str


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("EXERCISE", "EXERCISE"),
        ("Exercise", "EXERCISE"),
        ("1.2 EXERCISE", "EXERCISE"),
        ("EXERCISE 1.2", "EXERCISE"),
        ("(C) Exercise", "EXERCISE"),
        ("(C)\nExercise", "EXERCISE"),
        ("= EXERCISE 11.1", "EXERCISE"),
        ("Figure it out", "FIGURE_IT_OUT"),
        ("Example 1", "EXAMPLE"),
        ("Activity 2", "ACTIVITY"),
        ("Sample Question 3", "SAMPLE_QUESTION"),
        ("Short Answer", "SHORT_ANSWER"),
        ("Short Answer Type", "SHORT_ANSWER"),
        ("Long Answer", "LONG_ANSWER"),
        ("Long Answer Type", "LONG_ANSWER"),
        ("Completely unrelated text", "NONE"),
    ],
)
def test_classify_header_supports_supported_formats(text: str, expected: str) -> None:
    parser = SectionParser([])

    assert parser._classify_header(text) == expected


def test_parse_uses_header_state_machine() -> None:
    blocks = [
        Block(1, "EXERCISE 1.2"),
        Block(1, "1. First question"),
        Block(1, "Example 1"),
        Block(1, "ignored example text"),
        Block(2, "Figure it out"),
        Block(2, "2. Second question"),
        Block(2, "Activity"),
        Block(3, "Sample Question 1"),
        Block(3, "Short Answer"),
        Block(3, "Long Answer Type"),
        Block(4, "(C)\nExercise"),
        Block(4, "3. Third question"),
        Block(5, "= EXERCISE 11.1"),
        Block(5, "4. Fourth question"),
    ]

    sections = SectionParser(blocks).parse()

    assert [section.title for section in sections] == [
        "EXERCISE 1.2",
        "Figure it out",
        "(C) Exercise",
        "= EXERCISE 11.1",
    ]
    assert [len(section.blocks) for section in sections] == [1, 1, 1, 1]
    assert sections[0].blocks[0].text == "1. First question"
    assert sections[1].blocks[0].text == "2. Second question"
    assert sections[2].blocks[0].text == "3. Third question"
    assert sections[3].blocks[0].text == "4. Fourth question"