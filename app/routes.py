import mimetypes
from flask import Blueprint, Response, request, jsonify
from pathlib import Path

from .services.validate import validate_upload
from .services.decoder import decode_image
from .services.encoder import encode_image
from .services.processor import grayscale
from .services.exceptions import ValidationError, EncodingError

main = Blueprint("main", __name__)


@main.route("/")
def index():
    return jsonify({"status": "ok"})


@main.route("/images", methods=["POST"])
def images():
    try:
        file = validate_upload(request)
        data = file.read()
        image = decode_image(data)
    except ValidationError as err:
        return jsonify({"error": str(err)}), 400

    processed = grayscale(image)
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
