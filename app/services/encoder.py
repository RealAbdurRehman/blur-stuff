import cv2

from .exceptions import EncodingError, ValidationError


def encode_image(image, extension=".png"):
    if not cv2.haveImageWriter(f"dummy{extension}"):
        raise ValidationError("Unsupported image format")

    success, encoded = cv2.imencode(extension, image)

    if not success:
        raise EncodingError("Could not encode image")

    return encoded.tobytes()
