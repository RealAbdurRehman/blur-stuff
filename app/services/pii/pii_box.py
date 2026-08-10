from dataclasses import dataclass

from app.services.detectors.bounding_box import BoundingBox


@dataclass(slots=True)
class PIIBox(BoundingBox):
    type: str | None = None
    text: str | None = None
