import re

from .base import BaseDetector
from app.services.pii.types import DetectionType
from app.services.pii.detection import Detection

PHONE_PATTERN = re.compile(r"^\+?\d[\d()\-\s]{7,}\d$")


def clean_phone(text):
    return text.strip(".,;:!?")


class PhoneDetector(BaseDetector):

    def detect(self, graph):
        results = []
        visited = set()
        for token in graph.tokens:
            if token.id in visited:
                continue

            if not any(ch.isdigit() for ch in token.text):
                continue

            current = token
            candidate_tokens = []
            while current:
                if (
                    current.distance_to_next is not None
                    and current.distance_to_next > 40
                ):
                    break

                text = clean_phone(current.text)
                if not any(ch.isdigit() for ch in text):
                    break

                candidate_tokens.append(current)
                candidate = " ".join(clean_phone(t.text) for t in candidate_tokens)
                if PHONE_PATTERN.fullmatch(candidate):
                    for t in candidate_tokens:
                        visited.add(t.id)

                    results.append(
                        Detection(
                            type=DetectionType.PHONE,
                            text=candidate,
                            tokens=candidate_tokens.copy(),
                        )
                    )

                    break

                current = current.next

        return results
