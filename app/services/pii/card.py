import re

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


def clean_card(text):
    return text.strip()


def is_card(text):
    return CARD_PATTERN.fullmatch(text) is not None and luhn_check(text)


def detect_cards(tokens):
    results = []
    visited = set()

    for token in tokens:

        if token.id in visited:
            continue

        if not token.text[:1].isdigit():
            continue

        candidate_tokens = []
        current = token

        while current:

            if current.distance_to_next is not None and current.distance_to_next > 40:
                break

            text = clean_card(current.text)

            if not any(ch.isdigit() for ch in text):
                break

            candidate_tokens.append(current)

            candidate = " ".join(clean_card(t.text) for t in candidate_tokens)

            if is_card(candidate):

                for t in candidate_tokens:
                    visited.add(t.id)

                results.append(
                    {
                        "type": "CARD",
                        "text": candidate,
                        "tokens": candidate_tokens.copy(),
                    }
                )
                break

            current = current.next

    return results
