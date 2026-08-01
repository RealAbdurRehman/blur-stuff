import cv2
import numpy as np


def apply_overlay(image, boxes, overlay, padding=0):
    image_h, image_w = image.shape[:2]
    for box in boxes:
        bw = box.x2 - box.x1
        bh = box.y2 - box.y1

        size = int(max(bw, bh) * (1 + 2 * padding))
        if size <= 0:
            continue

        cx = (box.x1 + box.x2) / 2
        cy = (box.y1 + box.y2) / 2

        left = int(round(cx - size / 2))
        top = int(round(cy - size / 2))

        resized = cv2.resize(overlay, (size, size), interpolation=cv2.INTER_AREA)

        img_x1 = max(0, left)
        img_y1 = max(0, top)
        img_x2 = min(image_w, left + size)
        img_y2 = min(image_h, top + size)
        if img_x1 >= img_x2 or img_y1 >= img_y2:
            continue

        emoji_x1 = img_x1 - left
        emoji_y1 = img_y1 - top
        emoji_x2 = emoji_x1 + (img_x2 - img_x1)
        emoji_y2 = emoji_y1 + (img_y2 - img_y1)

        emoji = resized[emoji_y1:emoji_y2, emoji_x1:emoji_x2]
        roi = image[img_y1:img_y2, img_x1:img_x2]

        if emoji.shape[2] == 4:
            alpha = emoji[:, :, 3].astype(np.float32) / 255.0
            alpha = alpha[..., None]

            roi[:] = (
                emoji[:, :, :3].astype(np.float32) * alpha
                + roi.astype(np.float32) * (1.0 - alpha)
            ).astype(np.uint8)
        else:
            roi[:] = emoji

    return image
