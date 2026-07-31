from .pipeline import detect
from .effects.blur import blur_regions
from .video_state import VideoState

BLUR_CONFIG = {
    "faces": {
        "padding": 0.3,
    },
    "plates": {
        "padding": 0.08,
    },
    "text": {
        "padding": 0.1,
    },
    "pii": {
        "padding": 0.1,
    },
}

DETECTION_INTERVAL = 60


def apply_anonymization(image, detections, targets):
    for target in targets:
        blur_regions(image, detections[target], **BLUR_CONFIG[target])


def anonymize_image(image, targets):
    detections = detect(image, targets)
    apply_anonymization(image, detections, targets)

    return image


def anonymize_video(video, targets):
    state = VideoState()
    for frame in video.frames():
        tracker_lost = False
        if state.frame_number > 0:
            tracker_lost = state.tracker.update(frame)

        if state.should_detect(frame, DETECTION_INTERVAL, tracker_lost):
            detections = detect(frame, targets)
            state.tracker.initialize(frame, detections)
        else:
            detections = state.tracker.detections()

        apply_anonymization(frame, detections, targets)
        video.write(frame)

        state.next_frame(frame)

    return video
