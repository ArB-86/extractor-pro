from abc import ABC, abstractmethod


class OCRBase(ABC):

    @abstractmethod
    def recognize(self, image_path: str) -> str:
        pass
