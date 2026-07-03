from ultralytics import YOLO


def iou(a, b):
    x1 = max(a["x1"], b["x1"])
    y1 = max(a["y1"], b["y1"])
    x2 = min(a["x2"], b["x2"])
    y2 = min(a["y2"], b["y2"])

    inter = max(0, x2 - x1) * max(0, y2 - y1)

    area_a = (a["x2"] - a["x1"]) * (a["y2"] - a["y1"])
    area_b = (b["x2"] - b["x1"]) * (b["y2"] - b["y1"])

    return inter / (area_a + area_b - inter + 1e-6)


def non_max_suppression(boxes, iou_threshold=0.4):
    boxes = sorted(boxes, key=lambda x: x["confidence"], reverse=True)
    kept = []

    while boxes:
        best = boxes.pop(0)
        kept.append(best)

        boxes = [b for b in boxes if iou(best, b) < iou_threshold]

    return kept


class YoloDetector:
    def __init__(self, model_path, imgsizes=[1280], conf_threshold=0.5, augment=True):
        self.ready = True

        try:
            self.model = YOLO(model_path)
        except Exception:
            self.model = None
            self.ready = False

        self.imgsizes = imgsizes
        self.conf_threshold = conf_threshold
        self.augment = augment

    def detect(self, image):
        if self.model is None:
            raise RuntimeError("Detector unavailable")

        boxes = []

        for size in self.imgsizes:
            results = self.model(
                image,
                imgsz=size,
                conf=self.conf_threshold,
                augment=self.augment,
                verbose=False,
            )

            for result in results:
                for box in result.boxes:
                    x1, y1, x2, y2 = box.xyxy[0].tolist()

                    boxes.append(
                        {
                            "x1": int(x1),
                            "y1": int(y1),
                            "x2": int(x2),
                            "y2": int(y2),
                            "confidence": float(box.conf[0]),
                        }
                    )

        return non_max_suppression(boxes)
