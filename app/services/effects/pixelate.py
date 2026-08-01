import cv2

from .apply import apply_effect


def pixelate_regions(image, boxes, padding, fade_ratio, blocks=8):
    def pixelate(roi):
        h, w = roi.shape[:2]
        small = cv2.resize(roi, (blocks, blocks), interpolation=cv2.INTER_LINEAR)

        return cv2.resize(small, (w, h), interpolation=cv2.INTER_NEAREST)

    return apply_effect(image, boxes, pixelate, padding=padding, fade_ratio=fade_ratio)
