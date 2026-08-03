from app.services.processor import process_frame
from app.services.video_state import VideoState


def anonymize_image(media, targets, mode):
    state = VideoState()
    if media.animated:
        processed = []
        for frame in media.frames:
            process_frame(frame, state, targets, mode)
            processed.append(frame)

        media.frames = processed
        return media

    process_frame(media.image, state, targets, mode)
    return media
