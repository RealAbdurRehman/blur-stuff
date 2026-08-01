import numpy as np

from .apply import apply_effect


def noise_regions(image, boxes, padding=0, fade_ratio=0.15):
    def add_noise(roi):
        return np.random.randint(0, 256, roi.shape, dtype=np.uint8)

    return apply_effect(image, boxes, add_noise, padding, fade_ratio)
