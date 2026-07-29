import cv2
import easyocr


def is_useful_token(token):
    return any(ch.isalnum() for ch in token)


def resize(image, max_side=1500):
    h, w = image.shape[:2]
    longest = max(h, w)

    if longest <= max_side:
        return image, 1.0

    scale = max_side / longest
    resized = cv2.resize(
        image,
        (int(w * scale), int(h * scale)),
        interpolation=cv2.INTER_AREA,
    )

    return resized, scale


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

        resized, scale = resize(image)
        results = self.model.readtext(
            resized,
            decoder="greedy",
            paragraph=False,
            text_threshold=self.text_threshold,
            low_text=self.low_text,
            mag_ratio=2,
        )

        words = []
        inv_scale = 1.0 / scale
        for box, text, confidence in results:
            if not is_useful_token(text):
                continue

            xs = [p[0] for p in box]
            ys = [p[1] for p in box]

            words.append(
                {
                    "text": text,
                    "x1": int(min(xs) * inv_scale),
                    "y1": int(min(ys) * inv_scale),
                    "x2": int(max(xs) * inv_scale),
                    "y2": int(max(ys) * inv_scale),
                    "confidence": float(confidence),
                }
            )

        return words
