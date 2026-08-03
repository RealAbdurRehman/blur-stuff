import io
import cv2
import numpy as np

from PIL import Image as PILImage, ImageOps, ImageSequence
from pillow_heif import register_heif_opener

register_heif_opener()

from app.media import Image
from app.services.exceptions import ValidationError


def _pil_to_cv(image):
    image = ImageOps.exif_transpose(image)
    image = image.convert("RGB")
    return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)


def decode_image(data):
    try:
        image = PILImage.open(io.BytesIO(data))
        if getattr(image, "is_animated", False):
            frames = []
            durations = []
            loop = image.info.get("loop", 0)
            for frame in ImageSequence.Iterator(image):
                frames.append(_pil_to_cv(frame))
                durations.append(frame.info.get("duration", 100))

            return Image(frames=frames, durations=durations, loop=loop)

        return Image(_pil_to_cv(image))
    except Exception:
        raise ValidationError("Invalid image")
