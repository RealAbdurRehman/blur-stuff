from .pipeline import detect, assign_detection_ids
from .processor import process_frame
from .video_state import VideoState


def detect_image(image, targets):
    return detect(image, targets)


def detect_video(video, targets):
    state = VideoState(max(1, round(video.fps)))
    results = []
    for frame in video.frames():
        detections = process_frame(frame, state, targets)
        if detections is not None:
            results.append({"frame": state.frame_number, "detections": detections})

        state.next_frame(frame)

    return results


def detect_document(document, targets):
    results = []
    counters = {}
    for page in document:
        detections = detect(page.image, targets, assign_ids=False)
        assign_detection_ids(detections, counters)
        results.append({**detections, "page": page.number})

    return results
