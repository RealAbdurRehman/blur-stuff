import json

from pathlib import Path
from .exceptions import ValidationError


def validate_upload(req, allowed_extensions):
    if "file" not in req.files:
        raise ValidationError("No file uploaded")

    file = req.files["file"]
    if file.filename == "":
        raise ValidationError("File must have a name")

    extension = Path(file.filename).suffix.lower()
    if extension not in allowed_extensions:
        raise ValidationError("Unsupported file type")

    return file


DEFAULT_TARGETS = {"faces"}
SUPPORTED_TARGETS = {"faces", "plates", "text", "pii"}


def get_targets(request):
    value = request.args.get("targets")

    if value is None:
        return DEFAULT_TARGETS.copy()

    targets = {target.strip().lower() for target in value.split(",") if target.strip()}

    unknown = targets - SUPPORTED_TARGETS
    if unknown:
        raise ValidationError(f"Unsupported targets: {', '.join(sorted(unknown))}")

    if "text" in targets and "pii" in targets:
        raise ValidationError("Targets 'text' and 'pii' cannot be used together")

    return targets


SUPPORTED_MODES = {"pixelate", "blur", "solid", "noise", "emoji", "inpaint"}


def get_mode(request):
    mode = request.args.get("mode", "pixelate").strip().lower()
    if mode not in SUPPORTED_MODES:
        raise ValidationError(
            f"Unsupported mode '{mode}. Supported modes: {', '.join(sorted(SUPPORTED_MODES))}'"
        )

    return mode


DEFAULT_PADDING = 0.2
MIN_PADDING = 0.0
MAX_PADDING = 1.0


def get_padding(request):
    value = request.args.get("padding", type=float)
    if value is None:
        return DEFAULT_PADDING

    if not MIN_PADDING <= value <= MAX_PADDING:
        raise ValidationError(
            f"Padding must be between {MIN_PADDING} and {MAX_PADDING}"
        )

    return value


def get_selected_detections(request):
    raw = request.form.get("detections")
    if not raw:
        raise ValidationError("No detections were provided")

    try:
        detections = json.loads(raw)
    except json.JSONDecodeError:
        raise ValidationError("Invalid detections JSON")

    if not isinstance(detections, list):
        raise ValidationError("Detections must be a list")

    for detection in detections:
        if not isinstance(detection, dict):
            raise ValidationError("Invalid detection")

        target = detection.get("target")
        if target not in SUPPORTED_TARGETS:
            raise ValidationError(f"Unsupported detection target: {target}")

        for coordinate in ("x1", "y1", "x2", "y2"):
            if coordinate not in detection:
                raise ValidationError(f"Detection is missing {coordinate}")

            try:
                detection[coordinate] = float(detection[coordinate])
            except (TypeError, ValueError):
                raise ValidationError(f"Invalid detection coordinate: {coordinate}")

        if not (
            0 <= detection["x1"] < detection["x2"]
            and 0 <= detection["y1"] < detection["y2"]
        ):
            raise ValidationError(
                "Detection coordinates must define a valid bounding box"
            )

        frame = detection.get("frame")
        if frame is not None:
            try:
                detection["frame"] = int(frame)
            except (TypeError, ValueError):
                raise ValidationError("Invalid detection frame")

            if detection["frame"] < 0:
                raise ValidationError("Detection frame must be non-negative")

    return detections
