from .exceptions import ValidationError


def validate_upload(req, allowed_types):
    if "file" not in req.files:
        raise ValidationError("No file uploaded")

    file = req.files["file"]
    if file.filename == "":
        raise ValidationError("File must have a name")

    if file.content_type not in allowed_types:
        raise ValidationError("Unsupported file type")

    return file


SUPPORTED_TARGETS = {"faces", "plates", "text", "pii"}


def get_targets(request):
    value = request.form.get("targets")

    if value is None:
        return SUPPORTED_TARGETS.copy()

    targets = {target.strip().lower() for target in value.split(",") if target.strip()}

    unknown = targets - SUPPORTED_TARGETS
    if unknown:
        raise ValidationError(f"Unsupported targets: {', '.join(sorted(unknown))}")

    return targets
