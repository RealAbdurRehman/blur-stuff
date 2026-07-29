from .detector import YoloDetector

model = YoloDetector(model_path="models/plates.pt", conf_threshold=0.35)


def detect_plates(image):
    return model.detect(image)
