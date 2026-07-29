import cv2
import numpy as np

from .exceptions import ValidationError


def decode_image(data):
    image = cv2.imdecode(np.frombuffer(data, dtype=np.uint8), cv2.IMREAD_COLOR)

    if image is None:
        raise ValidationError("Invalid image")

    return image
