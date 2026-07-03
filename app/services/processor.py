from .pipeline import detect
from .effects.blur import blur_regions

BLUR_CONFIG = {
    "faces": {
        "padding": 0.2,
    },
    "plates": {
        "padding": 0.08,
    },
    "words": {
        "padding": 0.1,
    },
}


def anonymize(image, targets):
    detections = detect(image, targets)

    for target in targets:
        blur_regions(
            image,
            detections[target],
            **BLUR_CONFIG[target],
        )

    return image
