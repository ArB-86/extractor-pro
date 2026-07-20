from dataclasses import dataclass


@dataclass(slots=True)
class ExtractionContext:

    chapter: str | None = None

    chapter_number: int | None = None

    exercise: str | None = None

    page: int | None = None

    section: str | None = None

    block_type: str = "question"

    source_book: str | None = None

    class_name: int | None = None

    def update(self, result):

        if result.block_type == "chapter":
            self.chapter = result.chapter

        elif result.block_type == "exercise":
            self.exercise = result.exercise

        self.block_type = result.block_type
