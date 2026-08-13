import cv2
from itertools import count

from app.paths import NANOTRACK_HEAD
from app.paths import NANOTRACK_BACKBONE

from .tracked_object import TrackedObject
from app.services.effects.config import get_effect_config
from app.services.detectors.bounding_box import BoundingBox

MAX_LOST_FRAMES = 15


def create_tracker():
    params = cv2.TrackerNano_Params()
    params.neckhead = str(NANOTRACK_HEAD)
    params.backbone = str(NANOTRACK_BACKBONE)

    return cv2.TrackerNano_create(params)


class TrackerManager:
    def __init__(self):
        self.objects = []
        self.ids = count(1)

    def initialize(self, frame, detections, mode, padding=None):
        new_objects = []
        available = self.objects.copy()
        handled_targets = set(detections.keys())
        for target, boxes in detections.items():
            config = get_effect_config(mode, target, padding)
            for box in boxes:
                tracked = self.find_match(available, box, target)
                if tracked is not None:
                    available.remove(tracked)

                    box.id = tracked.box.id
                    old_trusted = tracked.trusted_box
                    new_tracker = create_tracker()
                    new_tracker.init(
                        frame,
                        (int(box.x1), int(box.y1), int(box.width), int(box.height)),
                    )

                    tracked.tracker = new_tracker
                    tracked.box = box
                    tracked.effect_config = config

                    tracked.lost = False
                    tracked.lost_frames = 0

                    if old_trusted is not None:
                        old_center = (
                            (old_trusted.x1 + old_trusted.x2) / 2,
                            (old_trusted.y1 + old_trusted.y2) / 2,
                        )

                        new_center = ((box.x1 + box.x2) / 2, (box.y1 + box.y2) / 2)
                        tracked.velocity = (
                            new_center[0] - old_center[0],
                            new_center[1] - old_center[1],
                        )

                    tracked.trusted_box = BoundingBox(
                        box.x1, box.y1, box.x2, box.y2, box.confidence
                    )

                    tracked.last_detection_frame = 0
                    new_objects.append(tracked)

                else:
                    box.id = f"{target}_{next(self.ids)}"
                    tracker = create_tracker()
                    tracker.init(
                        frame,
                        (int(box.x1), int(box.y1), int(box.width), int(box.height)),
                    )

                    center = ((box.x1 + box.x2) / 2, (box.y1 + box.y2) / 2)
                    trusted_box = BoundingBox(
                        box.x1, box.y1, box.x2, box.y2, box.confidence
                    )

                    new_objects.append(
                        TrackedObject(
                            target=target,
                            tracker=tracker,
                            box=box,
                            effect_config=config,
                            lost=False,
                            lost_frames=0,
                            trusted_box=trusted_box,
                            velocity=(0.0, 0.0),
                            last_detection_frame=0,
                        )
                    )

        for tracked in self.objects:
            if tracked.target not in handled_targets:
                new_objects.append(tracked)

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

    def update(self, frame, keep_lost=False):
        remaining = []
        lost_any = False
        for tracked in self.objects:
            ok, (x, y, w, h) = tracked.tracker.update(frame)
            if not ok:
                tracked.lost = True
                tracked.lost_frames += 1
                lost_any = True
                if keep_lost and tracked.lost_frames <= MAX_LOST_FRAMES:
                    remaining.append(tracked)

                continue

            tracked.box.x1 = float(x)
            tracked.box.y1 = float(y)
            tracked.box.x2 = float(x + w)
            tracked.box.y2 = float(y + h)

            tracked.lost = False
            tracked.lost_frames = 0

            remaining.append(tracked)

        self.objects = remaining

        return lost_any

    def __len__(self):
        return len(self.objects)

    def __iter__(self):
        return iter(self.objects)
