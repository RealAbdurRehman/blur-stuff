from flask import Blueprint, Response, request, jsonify

from app.services.media_types import VIDEO_TYPES
from app.services.validate import validate_upload, get_targets, get_mode
from app.services.decoder import decode_video
from app.services.encoder import encode_video
from app.services.anonymizer import anonymize_video
from app.services.exceptions import ValidationError

videos_bp = Blueprint("videos", __name__, url_prefix="/videos")


@videos_bp.post("/anonymize")
def videos():
    try:
        file = validate_upload(request, VIDEO_TYPES)
        video = decode_video(file)
    except ValidationError as err:
        return jsonify({"error": str(err)}), 400

    try:
        processed = anonymize_video(video, get_targets(request), get_mode(request))
    except RuntimeError as err:
        return jsonify({"error": str(err)}), 503

    encoded = encode_video(processed)

    return Response(
        encoded,
        mimetype="video/mp4",
        headers={"Content-Disposition": f'inline; filename="{file.filename}"'},
    )
