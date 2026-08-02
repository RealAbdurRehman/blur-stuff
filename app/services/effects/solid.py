import numpy as np

from .apply import apply_effect


def solid_regions(image, tracked, fade_ratio=0.15):
    def solid(roi):
        return np.zeros_like(roi)

    return apply_effect(image, tracked, solid, fade_ratio, False, False)
