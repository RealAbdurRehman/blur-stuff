import time

from .detectors.faces import detect_faces, unload_faces
from .detectors.plates import detect_plates, unload_plates
from .detectors.text import detect_text, unload_text
from .detectors.pii import detect_pii, unload_pii

DETECTORS = {
    "faces": (detect_faces, unload_faces),
    "plates": (detect_plates, unload_plates),
    "text": (detect_text, unload_text),
    "pii": (detect_pii, unload_pii),
}

ID_PREFIXES = {
    "faces": "face",
    "plates": "plate",
    "text": "token",
    "pii": "pii",
}


def assign_detection_ids(results, counters=None):
    if counters is None:
        counters = {}

    for target, items in results.items():
        prefix = ID_PREFIXES[target]
        counters.setdefault(target, 0)

        for item in items:
            counters[target] += 1
            item.id = f"{prefix}_{counters[target]}"

    return counters


def detect(image, targets, assign_ids=True):
    results = {}
    for target in targets:
        detector, unload = DETECTORS[target]

        start = time.time()
        try:
            results[target] = detector(image)
        finally:
            unload()

        print(f"[timing] {target}: {time.time() - start:.2f}s", flush=True)

    if assign_ids:
        assign_detection_ids(results)

    return results
