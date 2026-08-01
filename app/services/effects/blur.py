import cv2

from .apply import apply_effect


def blur_regions(image, boxes, padding=0, fade_ratio=0.15, kernel_size=51):
    if kernel_size % 2 == 0:
        kernel_size += 1

    def blur(roi):
        return cv2.blur(roi, (kernel_size, kernel_size))

    return apply_effect(image, boxes, blur, padding, fade_ratio)
