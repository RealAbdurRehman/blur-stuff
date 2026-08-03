import mimetypes
from pathlib import Path
from flask import Blueprint, Response, request, jsonify

from app.media.types import DOCUMENT_FORMATS
from app.services.validate import validate_upload, get_targets, get_mode
from app.services.converter import to_pdf
from app.services.decoder import decode_pdf
from app.services.encoder import encode_pdf
from app.services.anonymizer import anonymize_pdf
from app.services.exceptions import ValidationError, EncodingError

documents_bp = Blueprint("documents", __name__, url_prefix="/documents")

DOCUMENT_HANDLERS = {
    ".pdf": {
        "decoder": decode_pdf,
        "anonymizer": anonymize_pdf,
        "encoder": encode_pdf,
    },
}


@documents_bp.post("/anonymize")
def documents():
    try:
        file = validate_upload(request, DOCUMENT_FORMATS)
        extension = Path(file.filename).suffix.lower()

        data = file.read()
        if extension != ".pdf":
            data = to_pdf(data, extension)
            extension = ".pdf"

        handlers = DOCUMENT_HANDLERS.get(extension)
        if handlers is None:
            raise ValidationError("Unsupported document format")

        document = handlers["decoder"](data)
    except ValidationError as err:
        return jsonify({"error": str(err)}), 400

    try:
        processed = handlers["anonymizer"](
            document, get_targets(request), get_mode(request)
        )
    except RuntimeError as err:
        return jsonify({"error": str(err)}), 503

    try:
        encoded = handlers["encoder"](processed)
    except EncodingError as err:
        return jsonify({"error": str(err)}), 500

    mimetype = DOCUMENT_FORMATS[extension]
    return Response(
        encoded,
        mimetype=mimetype,
        headers={"Content-Disposition": f'inline; filename="{file.filename}"'},
    )
