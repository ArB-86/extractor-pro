
from abc import ABC, abstractmethod


class BaseProvider(ABC):

    @abstractmethod
    def generate(
        self,
        prompt,
        image=None,
        **kwargs
    ):
        pass
