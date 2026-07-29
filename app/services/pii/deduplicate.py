def overlaps(a, b):
    a_ids = {token.id for token in a.tokens}
    b_ids = {token.id for token in b.tokens}

    return not a_ids.isdisjoint(b_ids)


def score(detection):
    priority = {
        "EMAIL": 5,
        "PHONE": 4,
        "CARD": 3,
        "SSN": 3,
        "UUID": 2,
        "IPV4": 2,
        "IPV6": 2,
        "MAC": 2,
        "IBAN": 2,
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
