from .pipeline import detect
from .video_state import VideoState

from .effects.pixelate import pixelate_regions
from .effects.blur import blur_regions
from .effects.solid import solid_regions
from .effects.noise import noise_regions
from .effects.inpaint import inpaint_regions
from .overlays.emoji import emoji_regions

ANONYMIZATION_CONFIG = {
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

MODE_OVERRIDES = {
    "inpaint": {
        "faces": {
            "padding": 0.8,
        },
    }
}

ANONYMIZATION_MODES = {
    "pixelate": pixelate_regions,
    "blur": blur_regions,
    "solid": solid_regions,
    "noise": noise_regions,
    "emoji": emoji_regions,
    "inpaint": inpaint_regions,
}


def get_effect_config(mode, target):
    config = ANONYMIZATION_CONFIG[target].copy()
    override = MODE_OVERRIDES.get(mode, {}).get(target, {})
    config.update(override)

    return config


def apply_anonymization(image, detections, targets, mode):
    effect = ANONYMIZATION_MODES[mode]
    for target in targets:
        config = get_effect_config(mode, target)
        result = effect(image, detections[target], **config)

        if result is not None:
            image[:] = result


def anonymize_image(image, targets, mode):
    detections = detect(image, targets)
    apply_anonymization(image, detections, targets, mode)

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
            state.tracker.initialize(frame, detections)
        else:
            detections = state.tracker.detections()

        apply_anonymization(frame, detections, targets, mode)
        video.write(frame)

        state.next_frame(frame)

    return video
