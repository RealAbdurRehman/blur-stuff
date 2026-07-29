import cv2
import easyocr


def is_useful_token(token):
    return any(ch.isalnum() for ch in token)


class OcrDetector:
    def __init__(self, languages=("en",), text_threshold=0.4, low_text=0.2):
        self.ready = True

        try:
            self.model = easyocr.Reader(list(languages))
        except Exception:
            self.model = None
            self.ready = False

        self.text_threshold = text_threshold
        self.low_text = low_text

    def detect(self, image):
        if self.model is None:
            raise RuntimeError("OCR unavailable")

        results = self.model.readtext(
            image,
            decoder="greedy",
            paragraph=False,
            text_threshold=self.text_threshold,
            low_text=self.low_text,
            mag_ratio=2,
        )

        words = []

        for box, text, confidence in results:
            if not is_useful_token(text):
                continue

            xs = [p[0] for p in box]
            ys = [p[1] for p in box]

            words.append(
                {
                    "text": text,
                    "x1": int(min(xs)),
                    "y1": int(min(ys)),
                    "x2": int(max(xs)),
                    "y2": int(max(ys)),
                    "confidence": float(confidence),
                }
            )

        return words
