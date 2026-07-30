import re

from .base import BaseDetector
from app.services.pii.types import DetectionType
from app.services.pii.detection import Detection

URL_PATTERN = re.compile(
    r"(https?://\S+|www\.\S+)",
    re.IGNORECASE,
)


class UrlDetector(BaseDetector):
    def detect(self, graph):
        results = []

        for token in graph.tokens:
            if URL_PATTERN.search(token.text):
                results.append(
                    Detection(
                        type=DetectionType.URL,
                        text=token.text,
                        tokens=[token],
                    )
                )

        return results
