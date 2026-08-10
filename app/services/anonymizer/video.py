from app.services.processor import process_frames
from app.services.video_state import VideoState


def anonymize_video(video, targets, mode, padding):
    state = VideoState(max(1, round(video.fps)))

    for frame in process_frames(video.frames(), state, targets, mode, padding, False):
        video.write(frame)

    return video
