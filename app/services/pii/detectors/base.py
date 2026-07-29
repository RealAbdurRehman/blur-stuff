from abc import ABC, abstractmethod


class BaseDetector(ABC):
    @abstractmethod
    def detect(self, graph):
        pass
