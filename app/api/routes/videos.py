from flask import Blueprint, Response, request, jsonify

from app.media.types import VIDEO_FORMATS
from app.services.validate import validate_upload, get_targets, get_mode
from app.services.decoder import decode_video
from app.services.encoder import encode_video
from app.services.anonymizer import anonymize_video
from app.services.detector import detect_video
from app.services.exceptions import ValidationError

videos_bp = Blueprint("videos", __name__, url_prefix="/videos")


def load_video():
    file = validate_upload(request, VIDEO_FORMATS)
    video = decode_video(file)

    return file, video


@videos_bp.post("/detect")
def detections():
    try:
        _, video = load_video()

        targets = get_targets(request)
        detections = detect_video(video, targets)
    except ValidationError as err:
        return jsonify({"error": str(err)}), 400
    except RuntimeError as err:
        return jsonify({"error": str(err)}), 503

    return jsonify(detections)


@videos_bp.post("/anonymize")
def videos():
    try:
        file, video = load_video()

        targets = get_targets(request)
        mode = get_mode(request)
        processed = anonymize_video(video, targets, mode)
    except ValidationError as err:
        return jsonify({"error": str(err)}), 400
    except RuntimeError as err:
        return jsonify({"error": str(err)}), 503

    encoded = encode_video(processed)
    return Response(
        encoded,
        mimetype="video/mp4",
        headers={"Content-Disposition": f'inline; filename="{file.filename}"'},
    )
