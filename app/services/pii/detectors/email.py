import re

from .base import BaseDetector
from app.services.pii.types import DetectionType
from app.services.pii.detection import Detection

EMAIL_PATTERN = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")

LOCAL_RE = re.compile(r"^[A-Za-z0-9._%+-]+$")
DOMAIN_RE = re.compile(r"^[A-Za-z0-9-]+$")
TLD_RE = re.compile(r"^[A-Za-z]{2,}$")


def clean(text):
    return text.lower().strip(".,;:!?()[]{}")


def is_email(text):
    return EMAIL_PATTERN.fullmatch(text) is not None


class EmailDetector(BaseDetector):
    def detect(self, graph):
        results = []
        visited = set()
        for token in graph.tokens:
            if token.id in visited:
                continue

            if "@" not in token.normalized:
                continue

            email = self.build_email(token)

            if email is None:
                continue

            for t in email.tokens:
                visited.add(t.id)

            results.append(email)

        return results

    def build_email(self, at_token):
        left = self.collect_left(at_token)
        right = self.collect_right(at_token)

        if right is None:
            return None

        candidate = left["text"] + "@" + right["text"]
        if not is_email(candidate):
            return None

        return Detection(
            type=DetectionType.EMAIL,
            text=candidate,
            tokens=(left["tokens"] + [at_token] + right["tokens"]),
        )

    def collect_left(self, token):
        tokens = []
        parts = []
        current = token.previous
        while current:
            text = clean(current.text)

            if not LOCAL_RE.fullmatch(text):
                break

            if current.distance_to_next is not None and current.distance_to_next > 40:
                break

            tokens.insert(0, current)
            parts.insert(0, text)

            current = current.previous

        token_text = clean(token.text)
        local = ".".join(parts)
        if "@" in token_text:
            local_part = token_text.split("@", 1)[0]

            if local:
                local += "." + local_part
            else:
                local = local_part

        return {
            "text": local,
            "tokens": tokens,
        }

    def collect_right(self, token):
        token_text = clean(token.text)

        if "@" not in token_text:
            return None

        domain = token_text.split("@", 1)[1]
        parts = [domain]
        tokens = []

        current = token.next
        while current:
            text = clean(current.text)
            if TLD_RE.fullmatch(text):
                parts.append(text)
                tokens.append(current)
                break

            if not DOMAIN_RE.fullmatch(text):
                break

            if current.distance_to_next is not None and current.distance_to_next > 40:
                break

            parts.append(text)
            tokens.append(current)
            current = current.next

        return {
            "text": ".".join(parts),
            "tokens": tokens,
        }
