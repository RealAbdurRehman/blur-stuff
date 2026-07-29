from .detector import YoloDetector

model = YoloDetector(model_path="models/faces.pt", conf_threshold=0.05, prefix="face")


def detect_faces(image):
    return model.detect(image)
