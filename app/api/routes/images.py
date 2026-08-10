from pathlib import Path
from flask import Blueprint, Response, request, jsonify

from app.media.types import IMAGE_FORMATS
from app.services.validate import validate_upload, get_targets, get_mode, get_padding
from app.services.decoder import decode_image
from app.services.encoder import encode_image, encode_preview
from app.services.anonymizer import anonymize_image
from app.services.detector import detect_image
from app.services.exceptions import ValidationError, EncodingError

images_bp = Blueprint("images", __name__, url_prefix="/images")

OUTPUT_FORMATS = {".heic": ".png", ".heif": ".png"}


def load_image():
    file = validate_upload(request, IMAGE_FORMATS)
    media = decode_image(file.read())

    return file, media


@images_bp.post("/preview")
def preview():
    try:
        _, media = load_image()
    except ValidationError as err:
        return jsonify({"error": str(err)}), 400

    try:
        encoded = encode_preview(media)
    except EncodingError as err:
        return jsonify({"error": str(err)}), 500

    return Response(
        encoded,
        mimetype="image/png",
    )


@images_bp.post("/detect")
def detections():
    try:
        _, media = load_image()

        targets = get_targets(request)
        detections = detect_image(media.image, targets)
    except ValidationError as err:
        return jsonify({"error": str(err)}), 400
    except RuntimeError as err:
        return jsonify({"error": str(err)}), 503

    return jsonify(detections)


@images_bp.post("/anonymize")
def images():
    try:
        file, media = load_image()

        targets = get_targets(request)
        mode = get_mode(request)
        padding = get_padding(request)
        processed = anonymize_image(media, targets, mode, padding)
    except ValidationError as err:
        return jsonify({"error": str(err)}), 400
    except RuntimeError as err:
        return jsonify({"error": str(err)}), 503

    input_extension = Path(file.filename).suffix.lower()
    output_extension = OUTPUT_FORMATS.get(input_extension, input_extension)

    try:
        encoded = encode_image(processed, output_extension)
    except ValidationError as err:
        return jsonify({"error": str(err)}), 400
    except EncodingError as err:
        return jsonify({"error": str(err)}), 500

    mimetype = IMAGE_FORMATS[output_extension]
    output_filename = Path(file.filename).with_suffix(output_extension).name
    return Response(
        encoded,
        mimetype=mimetype,
        headers={"Content-Disposition": f'inline; filename="{output_filename}"'},
    )
