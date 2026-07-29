from .ocr import OcrDetector

model = OcrDetector()


def detect_words(image):
    return model.detect(image)
