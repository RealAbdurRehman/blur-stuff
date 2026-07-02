from .detectors.faces import detect_faces
from .detectors.plates import detect_plates

DETECTORS = {"faces": detect_faces, "plates": detect_plates}


def assign_ids(items, prefix):
    for i, item in enumerate(items, start=1):
        item["id"] = f"{prefix}_{i}"

    return items


def detect(image, targets):
    results = {}

    for target in targets:
        results[target] = assign_ids(DETECTORS[target](image), target)

    return results
