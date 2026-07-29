import re

EMAIL_PATTERN = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")

LOCAL_RE = re.compile(r"^[A-Za-z0-9._%+-]+$")
DOMAIN_RE = re.compile(r"^[A-Za-z0-9-]+$")
TLD_RE = re.compile(r"^[A-Za-z]{2,}$")


def clean(text):
    return text.lower().strip(".,;:!?()[]{}")


def is_email(text):
    return EMAIL_PATTERN.fullmatch(text) is not None


def detect_emails(tokens):
    results = []
    visited = set()

    for token in tokens:
        if token.id in visited:
            continue

        if "@" not in token.normalized:
            continue

        email = build_email(token)
        if email is None:
            continue

        for t in email["tokens"]:
            visited.add(t.id)

        results.append(email)

    return results


def build_email(at_token):
    left = collect_left(at_token)
    right = collect_right(at_token)

    candidate = left["text"] + "@" + right["text"]

    if not is_email(candidate):
        return None

    return {"text": candidate, "tokens": left["tokens"] + [at_token] + right["tokens"]}


def collect_left(token):
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

    local = ".".join(parts)
    token_text = clean(token.text)
    local_from_token = token_text.split("@", 1)[0]
    if local_from_token:
        if local:
            local += "." + local_from_token
        else:
            local = local_from_token

    return {
        "text": local,
        "tokens": tokens,
    }


def collect_right(token):
    token_text = clean(token.text)

    if "@" not in token_text:
        return None

    domain = token_text.split("@", 1)[1]
    pieces = [domain]

    tokens = []
    current = token.next
    while current:
        text = clean(current.text)

        if TLD_RE.fullmatch(text):
            if current.distance_to_next is not None and current.distance_to_next > 40:
                pieces.append(text)
                tokens.append(current)
                break

            pieces.append(text)
            tokens.append(current)
            break

        if not DOMAIN_RE.fullmatch(text):
            break

        if current.distance_to_next is not None and current.distance_to_next > 40:
            break

        pieces.append(text)
        tokens.append(current)

        current = current.next

    return {"text": ".".join(pieces), "tokens": tokens}
