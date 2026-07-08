from dataclasses import dataclass


@dataclass(slots=True)
class Taxonomy:

    topic: str | None = None

    subtopic: str | None = None

    blooms_level: str | None = None
