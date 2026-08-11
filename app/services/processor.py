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


def process_frame(
    image,
    state,
    targets,
    mode=None,
    padding=None,
    assign_ids=True,
    initial_detections=None,
    allow_detection=True,
):
    tracker_lost = False
    if state.frame_number > 0:
        tracker_lost = state.tracker.update(image)

    detections = None
    if initial_detections is not None:
        detections = initial_detections
        state.tracker.initialize(image, detections, mode, padding)
    elif allow_detection and state.should_detect(image, tracker_lost):
        detections = detect(image, targets, assign_ids)
        state.tracker.initialize(image, detections, mode, padding)

    if mode is not None:
        apply_anonymization(image, state.tracker, mode)

    return detections


def process_frames(frames, state, targets, mode, padding, assign_ids=True):
    for frame in frames:
        original_frame = frame.copy()
        process_frame(frame, state, targets, mode, padding, assign_ids)
        yield frame
        state.next_frame(original_frame)
