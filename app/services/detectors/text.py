from .ocr import OcrDetector

model = OcrDetector()


def detect_text(image):
    return model.detect(image)
