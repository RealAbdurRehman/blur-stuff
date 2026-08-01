import numpy as np

from .apply import apply_effect


def solid(image, boxes, padding=0, fade_ratio=0.15):
    def solid(roi):
        return np.zeros_like(roi)

    return apply_effect(image, boxes, solid, padding, fade_ratio, False, False)
