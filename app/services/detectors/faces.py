from .detector import YoloDetector
from app.paths import FACE_MODEL

model = YoloDetector(model_path=str(FACE_MODEL), conf_threshold=0.4)


def detect_faces(image):
    return model.detect(image)
