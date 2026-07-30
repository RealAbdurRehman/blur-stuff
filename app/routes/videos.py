from flask import Blueprint, request, jsonify

from app.services.validate import validate_upload
from app.services.exceptions import ValidationError

VIDEO_TYPES = {
    "video/mp4",
    "video/quicktime",
    "video/x-msvideo",
    "video/x-matroska",
    "video/webm",
}

videos_bp = Blueprint("videos", __name__)


@videos_bp.post("/videos/anonymize")
def videos():
    try:
        file = validate_upload(request, VIDEO_TYPES)
    except ValidationError as err:
        return jsonify({"error": str(err)}), 400

    return file
