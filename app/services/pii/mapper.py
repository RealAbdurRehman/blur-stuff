from .pii_box import PIIBox


def tokens_to_box(tokens):
    return PIIBox(
        x1=min(t.x1 for t in tokens),
        y1=min(t.y1 for t in tokens),
        x2=max(t.x2 for t in tokens),
        y2=max(t.y2 for t in tokens),
        confidence=max(t.confidence for t in tokens),
    )


def match_to_box(match):
    tokens = match.tokens
    return PIIBox(
        text=" ".join(t.text for t in tokens),
        type=match.type.value,
        x1=min(t.x1 for t in tokens),
        y1=min(t.y1 for t in tokens),
        x2=max(t.x2 for t in tokens),
        y2=max(t.y2 for t in tokens),
        confidence=max(t.confidence for t in tokens),
    )


def map_matches(matches):
    return [match_to_box(match) for match in matches]
