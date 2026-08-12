from app.services.processor import (
    process_frames,
    process_frame,
    process_selected_frame,
)
from app.services.video_state import VideoState


def anonymize_video(video, targets, mode, padding):
    state = VideoState(max(1, round(video.fps)))
    for frame in process_frames(video.frames(), state, targets, mode, padding, False):
        video.write(frame)

    return video


def anonymize_selected_video(video, detections, mode, padding):
    state = VideoState(max(1, round(video.fps)))
    if not detections:
        return video

    first_selected_frame = min(detections.keys())
    selected_targets = set()
    for frame_detections in detections.values():
        for detection in frame_detections:
            selected_targets.add(detection["target"])

    for frame_number, frame in enumerate(video.frames()):
        original_frame = frame.copy()
        if frame_number < first_selected_frame:
            video.write(frame)
            state.next_frame(original_frame)
            continue

        if frame_number == first_selected_frame:
            frame_detections = detections[frame_number]
            initial_detections = {}
            for detection in frame_detections:
                target = detection["target"]
                box = detection["box"]
                initial_detections.setdefault(target, []).append(box)

            process_selected_frame(
                frame,
                state,
                selected_targets,
                mode,
                padding,
                initial_detections=initial_detections,
            )
        else:
            process_selected_frame(frame, state, selected_targets, mode, padding)

        video.write(frame)
        state.next_frame(original_frame)

    return video
