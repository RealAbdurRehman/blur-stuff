from .detectors.faces import detect_faces


def detect(image):
    return {"faces": detect_faces(image)}
