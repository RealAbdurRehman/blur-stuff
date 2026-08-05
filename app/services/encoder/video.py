from pathlib import Path
from app.services.audio import merge_audio


def encode_video(video):
    video.close()
    merged = merge_audio(video.input_path, video.output_path)

    try:
        with open(merged, "rb") as f:
            return f.read()
    finally:
        for path in (video.input_path, video.output_path, merged):
            Path(path).unlink(missing_ok=True)
