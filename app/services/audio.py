import subprocess
import tempfile


def merge_audio(original_video, processed_video):
    output = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4").name
    command = [
        "ffmpeg",
        "-y",
        "-i",
        original_video,
        "-i",
        processed_video,
        "-map",
        "1:v:0",
        "-map",
        "0:a?",
        "-c:v",
        "copy",
        "-c:a",
        "aac",
        "-shortest",
        output,
    ]

    subprocess.run(
        command,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=True,
    )

    return output
