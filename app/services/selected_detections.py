from app.services.detectors.bounding_box import BoundingBox


def parse_selected_detections(data):
    detections = {}
    for detection in data:
        target = detection["target"]
        box = BoundingBox(
            detection["x1"],
            detection["y1"],
            detection["x2"],
            detection["y2"],
            detection.get("confidence", 1.0),
        )

        box.id = detection.get("id")
        detections.setdefault(target, []).append(box)

    return detections


def parse_selected_video_detections(data):
    detections = {}
    for detection in data:
        frame = detection.get("frame")
        if frame is None:
            continue

        box = BoundingBox(
            detection["x1"],
            detection["y1"],
            detection["x2"],
            detection["y2"],
            detection.get("confidence", 1.0),
        )
        box.id = detection.get("id")

        detections.setdefault(int(frame), []).append(
            {"target": detection["target"], "box": box}
        )

    return detections
