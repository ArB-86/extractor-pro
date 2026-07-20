from dataclasses import dataclass


@dataclass(slots=True)
class Chapter:

    class_name: int

    chapter_number: int

    chapter_name: str
