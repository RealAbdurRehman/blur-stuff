from .pipeline import detect
from .effects.blur import blur_regions

BLUR_CONFIG = {
    "faces": {
        "padding": 0.2,
    },
    "plates": {
        "padding": 0.08,
    },
    "text": {
        "padding": 0.1,
    },
    "pii": {
        "padding": 0.1,
    },
}


def anonymize_image(image, targets):
    detections = detect(image, targets)

    for target in targets:
        blur_regions(
            image,
            detections[target],
            **BLUR_CONFIG[target],
        )

    return image


def anonymize_video(video, targets):
    for frame in video.frames():
        processed = anonymize_image(frame, targets)
        video.write(processed)

    return video
