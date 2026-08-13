from dataclasses import dataclass, field

from app.services.detectors.bounding_box import BoundingBox


@dataclass
class TrackedObject:
    target: str
    tracker: object
    box: BoundingBox

    effect_config: dict = field(default_factory=dict)

    mask: object = None
    mask_rgb: object = None
    mask_size: tuple = None
    mask_full_size: tuple = None
    mask_offset: tuple = None

    lost: bool = False
    lost_frames: int = 0
    velocity: tuple = (0.0, 0.0)
    trusted_box: BoundingBox = None
    last_detection_frame: int = 0
