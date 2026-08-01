import cv2
import numpy as np


def apply_effect(image, boxes, effect, padding=0, fade_ratio=0.15):
    h, w = image.shape[:2]

    for box in boxes:
        x1, y1, x2, y2 = box.x1, box.y1, box.x2, box.y2
        bw, bh = x2 - x1, y2 - y1

        if padding:
            x1 -= int(bw * padding)
            y1 -= int(bh * padding)
            x2 += int(bw * padding)
            y2 += int(bh * padding)

        full_w, full_h = x2 - x1, y2 - y1

        fx1, fy1 = max(0.0, x1), max(0.0, y1)
        fx2, fy2 = min(float(w), x2), min(float(h), y2)
        if fx2 <= fx1 or fy2 <= fy1:
            continue

        cx1 = int(round(fx1))
        cy1 = int(round(fy1))
        cx2 = int(round(fx2))
        cy2 = int(round(fy2))
        roi = image[cy1:cy2, cx1:cx2]

        processed_roi = effect(roi)

        pad_px = int(min(bw, bh) * padding) if padding else 0
        feather_px = max(1, min(int(min(full_w, full_h) * fade_ratio), pad_px or 1))

        off_x, off_y = cx1 - x1, cy1 - y1

        rh, rw = roi.shape[:2]
        yy, xx = np.mgrid[0:rh, 0:rw].astype(np.float32)
        xx_full = xx + off_x
        yy_full = yy + off_y

        dist_to_edge = np.minimum(
            np.minimum(xx_full, full_w - 1 - xx_full),
            np.minimum(yy_full, full_h - 1 - yy_full),
        )
        mask = np.clip(dist_to_edge / feather_px, 0, 1)
        mask_3ch = cv2.merge([mask, mask, mask]).astype(np.float32)

        blended = (
            roi.astype(np.float32) * (1 - mask_3ch)
            + processed_roi.astype(np.float32) * mask_3ch
        ).astype(np.uint8)

        image[cy1:cy2, cx1:cx2] = blended

    return image
