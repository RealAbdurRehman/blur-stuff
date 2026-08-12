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


SELECTED_REDETECTION_INTERVAL = 3
SELECTED_MAX_RECOVERY_DISTANCE = 0.20


def _center(box):
    return ((box.x1 + box.x2) / 2, (box.y1 + box.y2) / 2)


def _predicted_center(tracked):
    center = tracked.last_center

    if center is None:
        center = _center(tracked.box)

    prediction_frames = min(tracked.lost_frames, 10)

    return (
        center[0] + tracked.velocity[0] * prediction_frames,
        center[1] + tracked.velocity[1] * prediction_frames,
    )


def _match_selected_detections(
    tracker,
    detections,
    image_shape,
):
    matched = {}
    height, width = image_shape[:2]
    diagonal = (width**2 + height**2) ** 0.5
    max_distance = diagonal * SELECTED_MAX_RECOVERY_DISTANCE
    used = {target: set() for target in detections}
    objects = sorted(tracker, key=lambda tracked: not tracked.lost)
    for tracked in objects:
        candidates = detections.get(tracked.target, [])
        if not candidates:
            continue

        predicted = _predicted_center(tracked)

        best_index = None
        best_distance = max_distance
        for index, detection in enumerate(candidates):
            if index in used.setdefault(tracked.target, set()):
                continue

            center = _center(detection)
            dx = center[0] - predicted[0]
            dy = center[1] - predicted[1]

            distance = (dx * dx + dy * dy) ** 0.5
            if distance < best_distance:
                best_distance = distance
                best_index = index

        if best_index is not None:
            detection = candidates[best_index]
            used[tracked.target].add(best_index)
            matched.setdefault(tracked.target, []).append(detection)

    return matched


def process_selected_frame(
    image, state, selected_targets, mode, padding, initial_detections=None
):
    if initial_detections is not None:
        state.tracker.initialize(image, initial_detections, mode, padding)
        if mode is not None:
            apply_anonymization(image, state.tracker, mode)

        return

    state.tracker.update(image, keep_lost=True)

    should_redetect = state.frame_number % SELECTED_REDETECTION_INTERVAL == 0
    if should_redetect:
        detections = detect(image, selected_targets, assign_ids=False)
        matched = _match_selected_detections(state.tracker, detections, image.shape)
        if matched:
            state.tracker.initialize(image, matched, mode, padding)

    if mode is not None:
        apply_anonymization(image, state.tracker, mode)


def process_selected_frames(frames, state, detections, mode, padding):
    frames = iter(frames)
    try:
        first_frame = next(frames)
    except StopIteration:
        return

    original_frame = first_frame.copy()
    process_selected_frame(
        first_frame,
        state,
        set(detections.keys()),
        mode,
        padding,
        initial_detections=detections,
    )

    yield first_frame

    state.next_frame(original_frame)
    for frame in frames:
        original_frame = frame.copy()
        process_selected_frame(frame, state, set(detections.keys()), mode, padding)
        yield frame

        state.next_frame(original_frame)


def process_selected_frames(frames, state, detections, mode, padding):
    frames = iter(frames)
    try:
        first_frame = next(frames)
    except StopIteration:
        return

    original_frame = first_frame.copy()
    process_selected_frame(
        first_frame,
        state,
        set(detections.keys()),
        mode,
        padding,
        initial_detections=detections,
    )

    yield first_frame

    state.next_frame(original_frame)
    for frame in frames:
        original_frame = frame.copy()
        process_selected_frame(frame, state, set(detections.keys()), mode, padding)
        yield frame

        state.next_frame(original_frame)
