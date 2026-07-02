from flask import Blueprint, request, jsonify

from app.services.validate import validate_upload
from app.services.decoder import decode_image
from app.services.detector import detect
from app.services.exceptions import ValidationError

detections_bp = Blueprint("detections", __name__)


@detections_bp.post("/images/detections")
def detections():
    try:
        file = validate_upload(request)
        image = decode_image(file.read())
    except ValidationError as err:
        return jsonify({"error": str(err)}), 400

    try:
        detections = detect(image)
    except RuntimeError as err:
        return jsonify({"error": str(err)}), 503

    return jsonify(detections)
