from app.services.processor import process_frame
from app.services.video_state import VideoState


def anonymize_video(video, targets, mode):
    state = VideoState(max(1, round(video.fps)))
    for frame in video.frames():
        process_frame(frame, state, targets, mode)
        video.write(frame)
        state.next_frame(frame)

    return video
