from dataclasses import dataclass, field
from typing import List

from src.schema.region import Region


@dataclass
class Document:

    pages: int

    regions: List[Region] = field(default_factory=list)

    def add_region(self, region: Region):

        self.regions.append(region)

    @property
    def text(self):

        return "\n\n".join(
            r.text
            for r in self.regions
            if r.text
        )

    @property
    def titles(self):

        return [
            r
            for r in self.regions
            if r.label == "title"
        ]

    @property
    def paragraphs(self):

        return [
            r
            for r in self.regions
            if r.label == "plain_text"
        ]
