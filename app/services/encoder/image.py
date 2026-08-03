import io
import cv2
from PIL import Image as PILImage

from app.services.exceptions import EncodingError, ValidationError

ANIMATED_IMAGE_FORMATS = {".gif": "GIF"}


def encode_image(media, extension=".png"):
    if media.animated:
        anim_format = ANIMATED_IMAGE_FORMATS.get(extension)
        if anim_format is None:
            raise ValidationError("Unsupported animated image format")

        output = io.BytesIO()
        frames = [
            PILImage.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            for frame in media.frames
        ]

        frames[0].save(
            output,
            format=anim_format,
            save_all=True,
            append_images=frames[1:],
            duration=media.durations,
            loop=media.loop,
        )

        return output.getvalue()

    if not cv2.haveImageWriter(f"dummy{extension}"):
        raise ValidationError("Unsupported image format")

    success, encoded = cv2.imencode(extension, media.image)
    if not success:
        raise EncodingError("Could not encode image")

    return encoded.tobytes()
