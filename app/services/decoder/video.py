from pathlib import Path

from app.media import Video


def decode_video(file):
    suffix = Path(file.filename).suffix
    return Video(file, suffix)
