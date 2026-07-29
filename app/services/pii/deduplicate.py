from .mapper import tokens_to_box


def overlaps(a, b):
    a_ids = {t.id for t in a.tokens}
    b_ids = {t.id for t in b.tokens}

    token_overlap = len(a_ids & b_ids)
    box_overlap = tokens_to_box(a.tokens).iou(tokens_to_box(b.tokens))

    return token_overlap >= min(len(a_ids), len(b_ids)) or box_overlap > 0.8


def score(detection):
    priority = {
        "EMAIL": 9,
        "PHONE": 8,
        "CARD": 8,
        "SSN": 8,
        "PERSON": 10,
        "ADDRESS": 7,
        "ORGANIZATION": 6,
        "LOCATION": 5,
        "IBAN": 4,
        "IPV4": 3,
        "IPV6": 3,
        "MAC": 3,
        "UUID": 3,
    }

    return (
        priority.get(detection.type.value, 0),
        len(detection.tokens),
    )


def deduplicate(detections):
    detections = sorted(
        detections,
        key=score,
        reverse=True,
    )

    result = []
    for detection in detections:
        duplicate = False

        for existing in result:
            if overlaps(existing, detection):
                duplicate = True
                break

        if not duplicate:
            result.append(detection)

    return result
