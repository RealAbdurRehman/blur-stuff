import time

from concurrent.futures import ThreadPoolExecutor

from .detectors.faces import detect_faces
from .detectors.plates import detect_plates
from .detectors.words import detect_words

DETECTORS = {"faces": detect_faces, "plates": detect_plates, "words": detect_words}


def assign_ids(items, prefix):
    for i, item in enumerate(items, start=1):
        item["id"] = f"{prefix}_{i}"

    return items


def detect(image, targets):
    results = {}

    with ThreadPoolExecutor(max_workers=len(targets) or 1) as executor:
        futures = {
            target: executor.submit(DETECTORS[target], image) for target in targets
        }

        for target, future in futures.items():
            start = time.time()
            results[target] = assign_ids(future.result(), target)
            print(f"[timing] {target}: {time.time() - start:.2f}s", flush=True)

    return results
