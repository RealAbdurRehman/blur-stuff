from app.services.detectors.bounding_box import BoundingBox


def tokens_to_box(tokens):
    return BoundingBox(
        id=tokens[0].id,
        text=" ".join(t.text for t in tokens),
        x1=min(t.x1 for t in tokens),
        y1=min(t.y1 for t in tokens),
        x2=max(t.x2 for t in tokens),
        y2=max(t.y2 for t in tokens),
        confidence=max(t.confidence for t in tokens),
    )


def map_matches(matches):
    return [tokens_to_box(match.tokens) for match in matches]
