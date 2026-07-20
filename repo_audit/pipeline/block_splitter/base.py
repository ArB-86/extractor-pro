from __future__ import annotations

from abc import ABC, abstractmethod

from pipeline.models import Paragraph


class BaseSplitter(ABC):

    name = "base"

    priority = 1000

    enabled = True

    @abstractmethod
    def split(self, blocks: list[Paragraph]) -> list[Paragraph]:
        raise NotImplementedError
