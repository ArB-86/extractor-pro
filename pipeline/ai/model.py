
from __future__ import annotations

from abc import ABC, abstractmethod


class VisionLanguageModel(ABC):

    @abstractmethod
    def generate(self, prompt, image=None):
        pass


class DummyModel(VisionLanguageModel):

    def generate(self, prompt, image=None):

        return {
            "status": "dummy",
            "response": prompt
        }
