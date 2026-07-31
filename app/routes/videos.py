from flask import Blueprint, Response, request, jsonify

from app.services.validate import validate_upload, get_targets
from app.services.decoder import decode_video
from app.services.encoder import encode_video
from app.services.processor import anonymize_video
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
    print(file := request.files["file"])
    print(file.filename)
    print(file.mimetype)

    try:
        file = validate_upload(request, VIDEO_TYPES)
        video = decode_video(file)
    except ValidationError as err:
        return jsonify({"error": str(err)}), 400

    try:
        processed = anonymize_video(video, get_targets(request))
    except RuntimeError as err:
        return jsonify({"error": str(err)}), 503

    encoded = encode_video(processed)

    return Response(
        encoded,
        mimetype="video/mp4",
        headers={"Content-Disposition": f'inline; filename="{file.filename}"'},
    )
