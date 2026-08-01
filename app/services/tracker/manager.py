import cv2

from .tracked_object import TrackedObject
from app.services.detectors.bounding_box import BoundingBox

HEAD = "models/nanotrack_head_sim.onnx"
BACKBONE = "models/nanotrack_backbone_sim.onnx"


def create_tracker():
    params = cv2.TrackerNano_Params()
    params.neckhead = HEAD
    params.backbone = BACKBONE

    return cv2.TrackerNano_create(params)


class TrackerManager:
    def __init__(self):
        self.objects = []

    def initialize(self, frame, detections):
        self.clear()

        for target, boxes in detections.items():
            for box in boxes:
                tracker = create_tracker()
                tracker.init(
                    frame,
                    (int(box.x1), int(box.y1), int(box.width), int(box.height)),
                )

                self.add(TrackedObject(target, tracker, box))

    def add(self, tracked_object):
        self.objects.append(tracked_object)

    def remove(self, tracked_object):
        self.objects.remove(tracked_object)

    def clear(self):
        self.objects.clear()

    def update(self, frame):
        remaining = []
        lost_any = False
        for tracked in self.objects:
            ok, (x, y, w, h) = tracked.tracker.update(frame)
            if not ok:
                lost_any = True
                continue

            tracked.box.x1 = float(x)
            tracked.box.y1 = float(y)
            tracked.box.x2 = float(x + w)
            tracked.box.y2 = float(y + h)

            remaining.append(tracked)

        self.objects = remaining

        return lost_any

    def detections(self):
        detections = {"faces": [], "plates": [], "text": [], "pii": []}
        for tracked in self.objects:
            detections[tracked.target].append(tracked.box)

        return detections

    def __len__(self):
        return len(self.objects)

    def __iter__(self):
        return iter(self.objects)
