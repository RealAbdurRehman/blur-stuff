from app.services.audio import merge_audio


def encode_video(video):
    video.close()
    merged = merge_audio(video.input_path, video.output_path)

    with open(merged, "rb") as f:
        return f.read()
