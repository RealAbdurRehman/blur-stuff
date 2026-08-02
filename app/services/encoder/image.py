import cv2

from app.services.exceptions import EncodingError, ValidationError


def encode_image(media, extension=".png"):
    if not cv2.haveImageWriter(f"dummy{extension}"):
        raise ValidationError("Unsupported image format")

    success, encoded = cv2.imencode(extension, media.image)
    if not success:
        raise EncodingError("Could not encode image")

    return encoded.tobytes()
