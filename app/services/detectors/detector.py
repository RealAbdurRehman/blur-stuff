from ultralytics import YOLO

from .bounding_box import BoundingBox


def non_max_suppression(boxes, iou_threshold=0.4):
    boxes = sorted(boxes, key=lambda b: b.confidence, reverse=True)

    kept = []
    while boxes:
        best = boxes.pop(0)
        kept.append(best)

        boxes = [b for b in boxes if best.iou(b) < iou_threshold]

    return kept


class YoloDetector:
    def __init__(self, model_path, imgsizes=[960], conf_threshold=0.5, augment=False):
        self.model_path = model_path
        self.imgsizes = imgsizes
        self.conf_threshold = conf_threshold
        self.augment = augment

        self.model = None
        self.ready = True
        self.load_error = None

    def _load_model(self):
        if self.model is not None:
            return

        try:
            self.model = YOLO(self.model_path)
        except Exception:
            self.model = None
            self.ready = False
            raise

    def unload(self):
        self.model = None

    def detect(self, image):
        self._load_model()

        boxes = []
        for size in self.imgsizes:
            results = self.model(
                image,
                imgsz=size,
                conf=self.conf_threshold,
                augment=self.augment,
                verbose=False,
                device="cpu",
            )

            for result in results:
                for box in result.boxes:
                    x1, y1, x2, y2 = box.xyxy[0].tolist()

                    boxes.append(
                        BoundingBox(
                            x1=int(x1),
                            y1=int(y1),
                            x2=int(x2),
                            y2=int(y2),
                            confidence=float(box.conf[0]),
                        )
                    )

            del result

        return non_max_suppression(boxes)
