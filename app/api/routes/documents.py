import cv2
from pathlib import Path
from flask import Blueprint, Response, request, jsonify

from app.media.types import DOCUMENT_FORMATS
from app.services.validate import validate_upload, get_targets, get_mode
from app.services.converter import to_pdf
from app.services.decoder import decode_pdf
from app.services.encoder import encode_pdf, encode_page_image
from app.services.anonymizer import anonymize_pdf
from app.services.detector import detect_document
from app.services.exceptions import ValidationError, EncodingError

documents_bp = Blueprint("documents", __name__, url_prefix="/documents")

DOCUMENT_HANDLERS = {
    ".pdf": {
        "decoder": decode_pdf,
        "anonymizer": anonymize_pdf,
        "encoder": encode_pdf,
    },
}


def load_document():
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

    return file, document, handlers, extension


@documents_bp.post("/preview")
def preview():
    try:
        _, document, handlers, _ = load_document()
    except ValidationError as err:
        return jsonify({"error": str(err)}), 400

    try:
        encoded = handlers["encoder"](document)
    except EncodingError as err:
        return jsonify({"error": str(err)}), 500

    return Response(
        encoded,
        mimetype="application/pdf",
    )


@documents_bp.post("/page-preview")
def page_preview():
    try:
        _, document, _, _ = load_document()
    except ValidationError as err:
        return jsonify({"error": str(err)}), 400

    page = request.args.get("page", type=int)
    if page is None or page < 1:
        return jsonify({"error": "Invalid page number"}), 400

    try:
        page = document.page(page - 1)
    except (IndexError, TypeError):
        return jsonify({"error": "Page not found"}), 404

    try:
        encoded = encode_page_image(page.image)
    except (EncodingError, ValidationError) as err:
        return jsonify({"error": str(err)}), 500

    return Response(
        encoded,
        mimetype="image/png",
    )


@documents_bp.post("/detect")
def detect():
    try:
        _, document, _, _ = load_document()

        targets = get_targets(request)
        detections = detect_document(document, targets)
    except ValidationError as err:
        return jsonify({"error": str(err)}), 400
    except RuntimeError as err:
        return jsonify({"error": str(err)}), 503

    return jsonify(detections)


@documents_bp.post("/anonymize")
def documents():
    try:
        file, document, handlers, extension = load_document()

        targets = get_targets(request)
        mode = get_mode(request)
        processed = handlers["anonymizer"](document, targets, mode)
    except ValidationError as err:
        return jsonify({"error": str(err)}), 400
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
