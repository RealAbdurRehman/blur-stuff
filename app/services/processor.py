from .pipeline import detect
from .video_state import VideoState

from .effects.config import get_effect_config
from .effects.pixelate import pixelate_regions
from .effects.blur import blur_regions
from .effects.solid import solid_regions
from .effects.noise import noise_regions
from .effects.inpaint import inpaint_regions
from .overlays.emoji import emoji_regions

ANONYMIZATION_MODES = {
    "pixelate": pixelate_regions,
    "blur": blur_regions,
    "solid": solid_regions,
    "noise": noise_regions,
    "emoji": emoji_regions,
    "inpaint": inpaint_regions,
}


def apply_anonymization(image, tracked_objects, mode):
    effect = ANONYMIZATION_MODES[mode]
    if mode == "inpaint":
        result = effect(image, tracked_objects)
        if result is not None:
            image[:] = result

        return

    for tracked in tracked_objects:
        effect(image, tracked)


def anonymize_image(image, targets, mode):
    detections = detect(image, targets)

    state = VideoState()
    state.tracker.initialize(image, detections, mode)

    apply_anonymization(image, state.tracker, mode)

    return image


def anonymize_video(video, targets, mode):
    state = VideoState()
    for frame in video.frames():
        tracker_lost = False
        if state.frame_number > 0:
            tracker_lost = state.tracker.update(frame)

        interval = max(1, round(video.fps))
        if state.should_detect(frame, interval, tracker_lost):
            detections = detect(frame, targets)
            state.tracker.initialize(frame, detections, mode)

        apply_anonymization(frame, state.tracker, mode)

        video.write(frame)
        state.next_frame(frame)

    return video
