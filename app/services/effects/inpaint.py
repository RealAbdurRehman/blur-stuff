import cv2
import numpy as np


def inpaint_regions(image, boxes, padding=0, radius=3):
    h, w = image.shape[:2]
    mask = np.zeros((h, w), dtype=np.uint8)
    for box in boxes:
        x1, y1, x2, y2 = (int(box.x1), int(box.y1), int(box.x2), int(box.y2))

        bw = x2 - x1
        bh = y2 - y1

        x1 -= int(bw * padding)
        y1 -= int(bh * padding)
        x2 += int(bw * padding)
        y2 += int(bh * padding)

        x1 = max(0, x1)
        y1 = max(0, y1)
        x2 = min(w, x2)
        y2 = min(h, y2)

        if x2 <= x1 or y2 <= y1:
            continue

        center = ((x1 + x2) // 2, (y1 + y2) // 2)
        axes = (max(1, (x2 - x1) // 2), max(1, (y2 - y1) // 2))
        cv2.ellipse(mask, center, axes, 0, 0, 360, 255, -1)

    return cv2.inpaint(image, mask, radius, cv2.INPAINT_TELEA)
