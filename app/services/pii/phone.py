import re

PHONE_PATTERN = re.compile(r"^\+?\d[\d()\-\s]{7,}\d$")


def clean_phone(text):
    return text.strip(".,;:!?")


def is_phone(text):
    return PHONE_PATTERN.fullmatch(text) is not None


def detect_phones(tokens):
    results = []
    visited = set()

    for token in tokens:
        if token.id in visited:
            continue

        if not any(ch.isdigit() for ch in token.text):
            continue

        current = token
        candidate_tokens = []
        while current:
            text = clean_phone(current.text)

            if current.distance_to_next is not None and current.distance_to_next > 40:
                break

            if not any(ch.isdigit() for ch in text):
                break

            candidate_tokens.append(current)
            candidate = " ".join(clean_phone(t.text) for t in candidate_tokens)
            if is_phone(candidate):
                for t in candidate_tokens:
                    visited.add(t.id)

                results.append(
                    {
                        "type": "PHONE",
                        "text": candidate,
                        "tokens": candidate_tokens.copy(),
                    }
                )
                break

            current = current.next

    return results
