import re

from .base import BaseDetector
from app.services.pii.types import DetectionType
from app.services.pii.detection import Detection

PATTERNS = {
    DetectionType.IPV4: {
        "pattern": re.compile(
            r"\b(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)"
            r"(?:\.(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}\b"
        )
    },
    DetectionType.IPV6: {
        "pattern": re.compile(r"\b(?:[0-9A-Fa-f]{1,4}:){2,7}" r"[0-9A-Fa-f]{1,4}\b")
    },
    DetectionType.MAC: {
        "pattern": re.compile(r"\b(?:[0-9A-Fa-f]{2}[:-]){5}" r"[0-9A-Fa-f]{2}\b")
    },
    DetectionType.UUID: {
        "pattern": re.compile(
            r"\b[0-9a-fA-F]{8}-"
            r"[0-9a-fA-F]{4}-"
            r"[1-5][0-9a-fA-F]{3}-"
            r"[89abAB][0-9a-fA-F]{3}-"
            r"[0-9a-fA-F]{12}\b"
        )
    },
    DetectionType.IBAN: {"pattern": re.compile(r"\b[A-Z]{2}\d{2}[A-Z0-9]{11,30}\b")},
    DetectionType.SSN: {"pattern": re.compile(r"\b\d{3}-\d{2}-\d{4}\b")},
}


class RegexDetector(BaseDetector):
    def detect(self, graph):
        results = []
        for line in graph.lines:
            for pii_type, config in PATTERNS.items():
                pattern = config["pattern"]
                for match in pattern.finditer(line.text):
                    tokens = []
                    for token in line.tokens:
                        if token.start < match.end() and token.end > match.start():
                            tokens.append(token)

                    if tokens:
                        results.append(
                            Detection(
                                type=pii_type,
                                text=match.group(),
                                tokens=tokens,
                            )
                        )

        return results
