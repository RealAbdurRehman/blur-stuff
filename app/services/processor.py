from .pipeline import detect

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


def process_frame(image, state, targets, mode=None):
    tracker_lost = False
    if state.frame_number > 0:
        tracker_lost = state.tracker.update(image)

    detections = None
    if state.should_detect(image, tracker_lost):
        detections = detect(image, targets)
        state.tracker.initialize(image, detections, mode)

    if mode is not None:
        apply_anonymization(image, state.tracker, mode)

    return detections


def process_frames(frames, state, targets, mode):
    for frame in frames:
        process_frame(frame, state, targets, mode)
        yield frame
        state.next_frame(frame)
