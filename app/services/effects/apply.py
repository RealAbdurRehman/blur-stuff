import cv2
import numpy as np


def rectangular_mask(width, height, feathered, fade_ratio):
    if not feathered:
        return np.ones((height, width), np.float32)

    yy, xx = np.mgrid[0:height, 0:width].astype(np.float32)
    feather = max(1, min(int(min(width, height) * fade_ratio), min(width, height) // 2))
    edge_dist = np.minimum.reduce([xx, width - 1 - xx, yy, height - 1 - yy])

    return np.clip(edge_dist / feather, 0, 1)


def elliptical_mask(
    width,
    height,
    full_width,
    full_height,
    offset_x,
    offset_y,
    feathered,
    fade_ratio,
    padding_px,
):
    yy, xx = np.mgrid[0:height, 0:width].astype(np.float32)

    xx += offset_x
    yy += offset_y

    rx = full_width / 2
    ry = full_height / 2

    distance = np.sqrt(((xx - rx) / rx) ** 2 + ((yy - ry) / ry) ** 2)
    if not feathered:
        return (distance <= 1).astype(np.float32)

    feather = max(
        1, min(int(min(full_width, full_height) * fade_ratio), padding_px or 1)
    )

    return np.clip(
        (1 - distance) / (feather / min(rx, ry)),
        0,
        1,
    )


def build_mask(
    shape,
    *,
    elliptical,
    feathered,
    fade_ratio,
    full_size=None,
    offset=None,
    padding_px=0,
):
    h, w = shape
    if not elliptical:
        return rectangular_mask(w, h, feathered, fade_ratio)

    full_w, full_h = full_size
    off_x, off_y = offset

    return elliptical_mask(
        w,
        h,
        full_w,
        full_h,
        off_x,
        off_y,
        feathered,
        fade_ratio,
        padding_px,
    )


def apply_effect(
    image, boxes, effect, padding=0, fade_ratio=0.15, feathered=True, elliptical=True
):
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
        pad_px = int(min(bw, bh) * padding) if padding else 0

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
        rh, rw = roi.shape[:2]

        mask = build_mask(
            (rh, rw),
            elliptical=elliptical,
            feathered=feathered,
            fade_ratio=fade_ratio,
            full_size=(full_w, full_h),
            offset=(cx1 - x1, cy1 - y1),
            padding_px=pad_px,
        )

        mask = cv2.merge([mask] * 3)

        blended = (
            roi.astype(np.float32) * (1.0 - mask)
            + processed_roi.astype(np.float32) * mask
        ).astype(np.uint8)

        image[cy1:cy2, cx1:cx2] = blended

    return image
