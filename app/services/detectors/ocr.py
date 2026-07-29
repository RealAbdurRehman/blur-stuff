import cv2
import easyocr
from itertools import count

from app.services.pii.token import Token


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
        languages=("en",),
        text_threshold=0.4,
        low_text=0.2,
    ):
        self.ready = True

        try:
            self.model = easyocr.Reader(list(languages))
        except Exception:
            self.model = None
            self.ready = False

        self.text_threshold = text_threshold
        self.low_text = low_text
        self._ids = count(1)

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

        tokens = []
        inv_scale = 1.0 / scale
        for box, text, confidence in results:
            if not is_useful_token(text):
                continue

            tokens.extend(
                self._split_token(
                    text=text,
                    box=box,
                    confidence=confidence,
                    inv_scale=inv_scale,
                )
            )

        return tokens

    def _split_token(
        self,
        text,
        box,
        confidence,
        inv_scale,
    ):
        parts = text.split()
        if len(parts) == 1:
            return [
                self._create_token(
                    text=text,
                    box=box,
                    confidence=confidence,
                    inv_scale=inv_scale,
                )
            ]

        x1 = min(point[0] for point in box)
        y1 = min(point[1] for point in box)
        x2 = max(point[0] for point in box)
        y2 = max(point[1] for point in box)

        tokens = []
        cursor = x1
        total_width = x2 - x1
        for part in parts:
            width_ratio = len(part) / len(text)
            part_width = total_width * width_ratio

            tokens.append(
                Token(
                    id=f"token_{next(self._ids)}",
                    text=part,
                    x1=int(cursor * inv_scale),
                    y1=int(y1 * inv_scale),
                    x2=int((cursor + part_width) * inv_scale),
                    y2=int(y2 * inv_scale),
                    confidence=confidence,
                )
            )

            cursor += part_width

        return tokens

    def _create_token(
        self,
        text,
        box,
        confidence,
        inv_scale,
    ):
        xs = [point[0] for point in box]
        ys = [point[1] for point in box]

        return Token(
            id=f"token_{next(self._ids)}",
            text=text,
            x1=int(min(xs) * inv_scale),
            y1=int(min(ys) * inv_scale),
            x2=int(max(xs) * inv_scale),
            y2=int(max(ys) * inv_scale),
            confidence=confidence,
        )
