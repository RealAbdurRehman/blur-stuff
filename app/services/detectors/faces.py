from .detector import YoloDetector

model = YoloDetector(model_path="models/faces.pt", conf_threshold=0.4)


def detect_faces(image):
    return model.detect(image)
