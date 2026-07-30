from .detectors.email import EmailDetector
from .detectors.url import UrlDetector
from .detectors.phone import PhoneDetector
from .detectors.card import CardDetector
from .detectors.regex import RegexDetector
from .detectors.presidio import PresidioDetector

from .deduplicate import deduplicate


class DetectorManager:
    def __init__(self):
        self.detectors = [
            EmailDetector(),
            UrlDetector(),
            PhoneDetector(),
            CardDetector(),
            RegexDetector(),
            PresidioDetector(),
        ]

    def detect(self, graph):
        results = []
        for detector in self.detectors:
            results.extend(detector.detect(graph))

        return deduplicate(results)
