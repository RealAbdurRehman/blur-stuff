from app.services.processor import process_frames, process_frame
from app.services.video_state import VideoState


def anonymize_video(video, targets, mode, padding):
    state = VideoState(max(1, round(video.fps)))
    for frame in process_frames(video.frames(), state, targets, mode, padding, False):
        video.write(frame)

    return video


def anonymize_selected_video(video, detections, mode, padding):
    state = VideoState(max(1, round(video.fps)))

    def selected_frames():
        for frame_number, frame in enumerate(video.frames()):
            selected = detections.get(frame_number)

            if selected:
                initial_detections = {}
                for detection in selected:
                    target = detection["target"]
                    box = detection["box"]

                    initial_detections.setdefault(target, []).append(box)

                yield frame, set(initial_detections.keys()), initial_detections
            else:
                yield frame, set(), None

    for frame, targets, initial_detections in selected_frames():
        process_frame(
            frame,
            state,
            targets,
            mode,
            padding,
            assign_ids=False,
            initial_detections=initial_detections,
            allow_detection=False,
        )

        video.write(frame)
        state.next_frame(frame)

    return video
