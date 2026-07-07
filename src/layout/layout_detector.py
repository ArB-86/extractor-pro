from abc import ABC, abstractmethod


class LayoutDetector(ABC):

    @abstractmethod
    def detect(self, image_path):
        pass
