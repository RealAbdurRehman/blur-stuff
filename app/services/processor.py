from .detectors.faces import detect_faces
from .effects.blur import blur_regions


def anonymize(image):
    boxes = detect_faces(image)
    return blur_regions(image, boxes)
