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


SUPPORTED_TARGETS = {"faces", "plates", "words"}


def get_targets(request):
    value = request.form.get("targets")

    if value is None:
        return SUPPORTED_TARGETS.copy()

    targets = {target.strip().lower() for target in value.split(",") if target.strip()}

    unknown = targets - SUPPORTED_TARGETS
    if unknown:
        raise ValidationError(f"Unsupported targets: {', '.join(sorted(unknown))}")

    return targets
