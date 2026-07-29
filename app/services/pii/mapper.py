from app.services.detectors.bounding_box import BoundingBox


def merge_boxes(tokens):
    return BoundingBox(
        id=tokens[0].id,
        x1=min(t.x1 for t in tokens),
        y1=min(t.y1 for t in tokens),
        x2=max(t.x2 for t in tokens),
        y2=max(t.y2 for t in tokens),
        confidence=max(t.confidence for t in tokens),
    )


def map_match(match):
    if "tokens" in match:
        return [token for token in match["tokens"]]

    start = match["start"]
    end = match["end"]

    tokens = []
    for token in match["line"]["tokens"]:
        if token["start"] < end and token["end"] > start:
            tokens.append(token["token"])

    return tokens


def map_matches(matches):
    boxes = []
    for match in matches:
        tokens = map_match(match)
        if not tokens:
            continue

        boxes.append(merge_boxes(tokens))

    return boxes
