from .detector import detect
from .effects.blur import blur_regions


def anonymize(image):
    detections = detect(image)
    return blur_regions(image, detections["faces"], padding=0.2)
