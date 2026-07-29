from .detectors.email import EmailDetector
from .detectors.phone import PhoneDetector
from .detectors.card import CardDetector
from .detectors.regex import RegexDetector

from .deduplicate import deduplicate


class DetectorManager:
    def __init__(self):
        self.detectors = [
            EmailDetector(),
            PhoneDetector(),
            CardDetector(),
            RegexDetector(),
        ]

    def detect(self, graph):
        results = []
        for detector in self.detectors:
            results.extend(detector.detect(graph))

        return deduplicate(results)
