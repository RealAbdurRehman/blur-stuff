from dataclasses import dataclass


@dataclass(slots=True)
class BoundingBox:
    id: str
    x1: float
    y1: float
    x2: float
    y2: float
    confidence: float

    @property
    def width(self):
        return self.x2 - self.x1

    @property
    def height(self):
        return self.y2 - self.y1

    @property
    def area(self):
        return self.width * self.height

    @property
    def center_x(self):
        return (self.x1 + self.x2) / 2

    @property
    def center_y(self):
        return (self.y1 + self.y2) / 2

    def iou(self, other):
        x1 = max(self.x1, other.x1)
        y1 = max(self.y1, other.y1)
        x2 = min(self.x2, other.x2)
        y2 = min(self.y2, other.y2)

        inter = max(0, x2 - x1) * max(0, y2 - y1)

        union = self.area + other.area - inter

        return inter / (union + 1e-6)
