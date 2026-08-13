from .detector import YoloDetector
from app.paths import PLATE_MODEL

model = YoloDetector(model_path=str(PLATE_MODEL), conf_threshold=0.5)


def detect_plates(image):
    return model.detect(image)
