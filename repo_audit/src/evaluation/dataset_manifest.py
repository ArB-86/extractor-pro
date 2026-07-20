from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from hashlib import sha256
import json


@dataclass(slots=True)
class DatasetManifest:

    dataset_name: str

    version: str

    total_questions: int

    books: list[str]

    files: list[str]

    sha256: str = ""

    metadata: dict = field(default_factory=dict)

    def compute(self):

        payload = json.dumps(
            {
                "dataset_name": self.dataset_name,
                "version": self.version,
                "total_questions": self.total_questions,
                "books": self.books,
                "files": self.files,
            },
            sort_keys=True,
        )

        self.sha256 = sha256(
            payload.encode()
        ).hexdigest()

        return self

    def save(self,path):

        self.compute()

        Path(path).write_text(
            json.dumps(
                self.__dict__,
                indent=2,
            ),
            encoding="utf-8",
        )
