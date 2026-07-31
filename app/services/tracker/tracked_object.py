from dataclasses import dataclass

from app.services.detectors.bounding_box import BoundingBox


@dataclass
class TrackedObject:
    target: str
    tracker: object
    box: BoundingBox
