import statistics

from app.services.video_state import VideoState
from app.services.processor import (
    process_frame,
    process_frames,
    process_selected_frames,
)


def anonymize_image(media, targets, mode, padding):
    if media.animated:
        average_duration = statistics.mean(media.durations)
        fps = max(1, round(1000 / average_duration))
        state = VideoState(fps)

        media.frames = list(process_frames(media.frames, state, targets, mode, padding))

        return media

    state = VideoState()
    process_frame(media.image, state, targets, mode, padding)

    return media


def anonymize_selected_image(media, detections, mode, padding):
    if media.animated:
        average_duration = statistics.mean(media.durations)
        fps = max(1, round(1000 / average_duration))
        state = VideoState(fps)
        media.frames = list(
            process_selected_frames(
                media.frames,
                state,
                detections,
                mode,
                padding,
            )
        )

        return media

    state = VideoState()
    process_frame(
        media.image,
        state,
        set(detections.keys()),
        mode,
        padding,
        initial_detections=detections,
        allow_detection=False,
    )

    return media
