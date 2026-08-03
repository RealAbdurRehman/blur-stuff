from pathlib import Path
from flask import Blueprint, Response, request, jsonify

from app.media.types import IMAGE_FORMATS
from app.services.validate import validate_upload, get_targets, get_mode
from app.services.decoder import decode_image
from app.services.encoder import encode_image
from app.services.anonymizer import anonymize_image
from app.services.exceptions import ValidationError, EncodingError

images_bp = Blueprint("images", __name__, url_prefix="/images")


@images_bp.post("/anonymize")
def images():
    try:
        file = validate_upload(request, IMAGE_FORMATS)
        media = decode_image(file.read())
    except ValidationError as err:
        return jsonify({"error": str(err)}), 400

    try:
        processed = anonymize_image(media, get_targets(request), get_mode(request))
    except RuntimeError as err:
        return jsonify({"error": str(err)}), 503

    extension = Path(file.filename).suffix.lower()

    try:
        encoded = encode_image(processed, extension)
    except ValidationError as err:
        return jsonify({"error": str(err)}), 400
    except EncodingError as err:
        return jsonify({"error": str(err)}), 500

    mimetype = IMAGE_FORMATS[extension]
    return Response(
        encoded,
        mimetype=mimetype,
        headers={"Content-Disposition": f'inline; filename="{file.filename}"'},
    )
