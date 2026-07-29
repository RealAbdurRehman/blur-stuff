import cv2
import numpy as np


def blur_regions(
    image,
    boxes,
    padding=0,
    fade_ratio=0.15,
):
    output = image.copy()
    h, w = image.shape[:2]

    for box in boxes:
        x1, y1, x2, y2 = box["x1"], box["y1"], box["x2"], box["y2"]

        if padding:
            bw, bh = x2 - x1, y2 - y1
            x1 -= int(bw * padding)
            y1 -= int(bh * padding)
            x2 += int(bw * padding)
            y2 += int(bh * padding)

        full_w, full_h = x2 - x1, y2 - y1

        cx1, cy1 = max(0, x1), max(0, y1)
        cx2, cy2 = min(w, x2), min(h, y2)
        if cx2 <= cx1 or cy2 <= cy1:
            continue

        roi = output[cy1:cy2, cx1:cx2]
        rh, rw = roi.shape[:2]

        blocks = 8
        small = cv2.resize(roi, (blocks, blocks), interpolation=cv2.INTER_LINEAR)
        processed_roi = cv2.resize(small, (rw, rh), interpolation=cv2.INTER_NEAREST)

        feather_px = max(1, int(min(full_w, full_h) * fade_ratio))

        off_x, off_y = cx1 - x1, cy1 - y1

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

        output[cy1:cy2, cx1:cx2] = blended

    return output
