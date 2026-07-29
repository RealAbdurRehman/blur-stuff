from dataclasses import dataclass, field

from .normalize import normalize_text
from app.services.detectors.bounding_box import BoundingBox


@dataclass(slots=True)
class Token(BoundingBox):
    text: str
    normalized: str = field(init=False)

    line_id: int = -1
    start: int = 0
    end: int = 0
    previous: str = field(default=None, repr=False)
    next: str = field(default=None, repr=False)

    def __post_init__(self):
        self.normalized = normalize_text(self.text)

    @property
    def distance_to_next(self):
        if not self.next:
            return None

        return self.next.x1 - self.x2
