import cv2
import numpy as np

from pathlib import Path
from .video import Video

from .exceptions import ValidationError


def decode_image(data):
    image = cv2.imdecode(np.frombuffer(data, dtype=np.uint8), cv2.IMREAD_COLOR)

    if image is None:
        raise ValidationError("Invalid image")

    return image


def decode_video(file):
    suffix = Path(file.filename).suffix
    return Video(file, suffix)
