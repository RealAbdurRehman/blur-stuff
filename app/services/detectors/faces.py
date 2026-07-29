from .detector import YoloDetector

model = YoloDetector(model_path="models/faces.pt")


def detect_faces(image):
    return model.detect(image)
