from .exceptions import ValidationError


def validate_upload(req):
    if "file" not in req.files:
        raise ValidationError("No file uploaded")

    file = req.files["file"]
    if file.filename == "":
        raise ValidationError("File must have a name")

    if not file.content_type.startswith("image/"):
        raise ValidationError("File must be an image")

    return file
