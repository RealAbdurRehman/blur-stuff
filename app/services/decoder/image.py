import io
import cv2
import numpy as np

from PIL import Image as PILImage, ImageOps, UnidentifiedImageError

from app.media import Image
from app.services.exceptions import ValidationError


def decode_image(data):
    try:
        image = PILImage.open(io.BytesIO(data))
        image = ImageOps.exif_transpose(image)
        image = image.convert("RGB")
        image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    except (UnidentifiedImageError, OSError, ValueError):
        raise ValidationError("Invalid image")

    return Image(image)
