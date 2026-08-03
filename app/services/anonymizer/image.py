import statistics

from app.services.video_state import VideoState
from app.services.processor import process_frame, process_frames


def anonymize_image(media, targets, mode):
    state = VideoState(60)
    if media.animated:
        processed = []
        for frame in media.frames:
            process_frame(frame, state, targets, mode)
            processed.append(frame)
            state.next_frame(frame)

        media.frames = processed
        return media

    process_frame(media.image, state, targets, mode)
    return media


def anonymize_image(media, targets, mode):
    if media.animated:
        average_duration = statistics.mean(media.durations)
        fps = max(1, round(1000 / average_duration))
        state = VideoState(fps)

        media.frames = list(process_frames(media.frames, state, targets, mode))

        return media

    state = VideoState()
    process_frame(media.image, state, targets, mode)

    return media
