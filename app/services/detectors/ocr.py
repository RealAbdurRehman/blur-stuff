import cv2
from itertools import count
from paddleocr import PaddleOCR

from app.services.pii.token import Token


def is_useful_token(token):
    return bool(token.strip())


def enhance(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)

    return cv2.cvtColor(enhanced, cv2.COLOR_GRAY2BGR)


def resize(image, max_side=960):
    h, w = image.shape[:2]
    longest = max(h, w)
    if longest <= max_side:
        return image, 1.0

    scale = max_side / longest
    resized = cv2.resize(
        image,
        (
            int(w * scale),
            int(h * scale),
        ),
        interpolation=cv2.INTER_AREA,
    )

    return resized, scale


class OcrDetector:
    def __init__(
        self,
        language="en",
    ):
        self.ready = True

        try:
            self.model = PaddleOCR(
                lang=language,
                text_detection_model_name="PP-OCRv6_small_det",
                text_recognition_model_name="latin_PP-OCRv5_mobile_rec",
                use_doc_orientation_classify=False,
                use_doc_unwarping=False,
                use_textline_orientation=False,
            )
        except Exception:
            self.model = None
            self.ready = False

        self._ids = count(1)

    def detect(self, image):
        enhanced = enhance(image)
        resized, scale = resize(enhanced)
        result = self.model.predict(resized)

        tokens = []
        inv_scale = 1.0 / scale
        for page in result:
            boxes = page["rec_boxes"]
            texts = page["rec_texts"]
            scores = page["rec_scores"]
            for box, text, confidence in zip(
                boxes,
                texts,
                scores,
            ):
                if not is_useful_token(text):
                    continue

                x1, y1, x2, y2 = box
                tokens.append(
                    Token(
                        id=f"token_{next(self._ids)}",
                        text=text,
                        x1=int(x1 * inv_scale),
                        y1=int(y1 * inv_scale),
                        x2=int(x2 * inv_scale),
                        y2=int(y2 * inv_scale),
                        confidence=float(confidence),
                    )
                )

        return tokens
