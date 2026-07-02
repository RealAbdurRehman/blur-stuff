import mimetypes
from pathlib import Path
from flask import Blueprint, Response, request, jsonify

from app.services.validate import validate_upload
from app.services.decoder import decode_image
from app.services.encoder import encode_image
from app.services.processor import anonymize
from app.services.exceptions import ValidationError, EncodingError

images_bp = Blueprint("images", __name__)


@images_bp.post("/images/anonymize")
def images():
    try:
        file = validate_upload(request)
        image = decode_image(file.read())
    except ValidationError as err:
        return jsonify({"error": str(err)}), 400

    try:
        processed = anonymize(image)
    except RuntimeError as err:
        return jsonify({"error": str(err)}), 503

    extension = Path(file.filename).suffix.lower()

    try:
        encoded = encode_image(processed, extension)
    except ValidationError as err:
        return jsonify({"error": str(err)}), 400
    except EncodingError as err:
        return jsonify({"error": str(err)}), 500

    mimetype, _ = mimetypes.guess_type(f"dummy{extension}")
    return Response(
        encoded,
        mimetype=mimetype,
        headers={"Content-Disposition": f'inline; filename="{file.filename}"'},
    )
