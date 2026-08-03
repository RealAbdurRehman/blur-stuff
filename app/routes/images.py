from pathlib import Path
from flask import Blueprint, Response, request, jsonify

from app.media.types import IMAGE_FORMATS
from app.services.validate import validate_upload, get_targets, get_mode
from app.services.decoder import decode_image
from app.services.encoder import encode_image
from app.services.anonymizer import anonymize_image
from app.services.exceptions import ValidationError, EncodingError

images_bp = Blueprint("images", __name__, url_prefix="/images")

OUTPUT_FORMATS = {".heic": ".png", ".heif": ".png"}


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
