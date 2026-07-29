import re

from .base import BaseDetector
from app.services.pii.types import DetectionType
from app.services.pii.detection import Detection

CARD_PATTERN = re.compile(r"^(?:\d[ -]?){13,19}$")


def luhn_check(number):
    digits = [int(d) for d in re.sub(r"\D", "", number)]

    if not (13 <= len(digits) <= 19):
        return False

    checksum = 0
    parity = len(digits) % 2
    for i, digit in enumerate(digits):
        if i % 2 == parity:
            digit *= 2

            if digit > 9:
                digit -= 9

        checksum += digit

    return checksum % 10 == 0


class CardDetector(BaseDetector):
    def detect(self, graph):
        results = []
        visited = set()
        for token in graph.tokens:
            if token.id in visited:
                continue

            if not token.text[:1].isdigit():
                continue

            current = token
            candidate_tokens = []
            while current:
                if (
                    current.distance_to_next is not None
                    and current.distance_to_next > 40
                ):
                    break

                if not any(ch.isdigit() for ch in current.text):
                    break

                candidate_tokens.append(current)
                candidate = " ".join(t.text for t in candidate_tokens)
                if CARD_PATTERN.fullmatch(candidate) and luhn_check(candidate):
                    for t in candidate_tokens:
                        visited.add(t.id)

                    results.append(
                        Detection(
                            type=DetectionType.CARD,
                            text=candidate,
                            tokens=candidate_tokens.copy(),
                        )
                    )

                    break

                current = current.next

        return results
