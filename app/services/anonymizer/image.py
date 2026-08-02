from app.services.processor import process_frame
from app.services.video_state import VideoState


def anonymize_image(media, targets, mode):
    state = VideoState()
    process_frame(media.image, state, targets, mode)

    return media
