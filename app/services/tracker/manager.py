import cv2
from itertools import count

from .tracked_object import TrackedObject
from app.services.effects.config import get_effect_config

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
        self.ids = count(1)

    def initialize(self, frame, detections, mode):
        new_objects = []
        available = self.objects.copy()
        for target, boxes in detections.items():
            config = get_effect_config(mode, target)
            for box in boxes:
                tracked = self.find_match(available, box, target)

                if tracked is not None:
                    available.remove(tracked)
                    box.id = tracked.box.id
                else:
                    box.id = f"{target}_{next(self.ids)}"

                tracker = create_tracker()
                tracker.init(
                    frame, (int(box.x1), int(box.y1), int(box.width), int(box.height))
                )

                new_objects.append(TrackedObject(target, tracker, box, config))

        self.objects = new_objects

    def find_match(self, available, box, target, threshold=0.3):
        best = None
        best_iou = threshold
        for tracked in available:
            if tracked.target != target:
                continue

            iou = tracked.box.iou(box)
            if iou > best_iou:
                best = tracked
                best_iou = iou

        return best

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

    def __len__(self):
        return len(self.objects)

    def __iter__(self):
        return iter(self.objects)
