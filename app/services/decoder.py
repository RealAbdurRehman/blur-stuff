import io
import cv2
import numpy as np

from pathlib import Path
from PIL import Image, ImageOps, UnidentifiedImageError

from .video import Video
from .exceptions import ValidationError


def decode_image(data):
    try:
        image = Image.open(io.BytesIO(data))
        image = ImageOps.exif_transpose(image)
        image = image.convert("RGB")
        image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    except (UnidentifiedImageError, OSError, ValueError):
        raise ValidationError("Invalid image")

    return image


def decode_video(file):
    suffix = Path(file.filename).suffix
    return Video(file, suffix)
