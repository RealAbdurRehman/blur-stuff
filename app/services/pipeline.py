import time

from concurrent.futures import ThreadPoolExecutor

from .detectors.faces import detect_faces
from .detectors.plates import detect_plates
from .detectors.text import detect_text
from .detectors.pii import detect_pii

DETECTORS = {
    "faces": detect_faces,
    "plates": detect_plates,
    "text": detect_text,
    "pii": detect_pii,
}


def detect(image, targets):
    results = {}

    with ThreadPoolExecutor(max_workers=len(targets) or 1) as executor:
        futures = {
            target: executor.submit(DETECTORS[target], image) for target in targets
        }

        for target, future in futures.items():
            start = time.time()
            results[target] = future.result()
            print(f"[timing] {target}: {time.time() - start:.2f}s", flush=True)

    return results
