import cv2
import numpy as np

PADDING_RATIO = 0.8

MASK_BLUR_KERNEL_SIZE = 23

MASK_COLOR = 255
MASK_RADIUS_X = 0.94
MASK_RADIUS_Y = 0.8


def add_padding(x1, y1, x2, y2, image_width, image_height):
    pad_x = int((x2 - x1) * PADDING_RATIO)
    pad_y = int((y2 - y1) * PADDING_RATIO)

    return (
        max(0, x1 - pad_x),
        max(0, y1 - pad_y),
        min(image_width, x2 + pad_x),
        min(image_height, y2 + pad_y),
    )


def pixelate(roi, blocks=12):
    h, w = roi.shape[:2]
    temp = cv2.resize(roi, (blocks, blocks), interpolation=cv2.INTER_LINEAR)

    return cv2.resize(temp, (w, h), interpolation=cv2.INTER_NEAREST)


def create_mask(roi_height, roi_width, center, face_height, face_width):
    mask = np.zeros((roi_height, roi_width), dtype=np.uint8)
    axes = (
        int(face_width * MASK_RADIUS_X),
        int(face_height * MASK_RADIUS_Y),
    )

    cv2.ellipse(
        mask,
        center,
        axes,
        angle=0,
        startAngle=0,
        endAngle=360,
        color=MASK_COLOR,
        thickness=-1,
    )

    mask = cv2.GaussianBlur(mask, (MASK_BLUR_KERNEL_SIZE, MASK_BLUR_KERNEL_SIZE), 0)
    mask = mask.astype(np.float32) / MASK_COLOR

    return mask[..., np.newaxis]


def blur_regions(image, boxes):
    image_height, image_width = image.shape[:2]

    for box in boxes:
        fx1, fy1 = box["x1"], box["y1"]
        fx2, fy2 = box["x2"], box["y2"]

        x1, y1, x2, y2 = add_padding(
            fx1,
            fy1,
            fx2,
            fy2,
            image_width,
            image_height,
        )

        roi = image[y1:y2, x1:x2]
        blurred = pixelate(roi)

        face_center_x = (fx1 + fx2) // 2 - x1
        face_center_y = (fy1 + fy2) // 2 - y1
        mask = create_mask(
            roi.shape[0],
            roi.shape[1],
            (face_center_x, face_center_y),
            fy2 - fy1,
            fx2 - fx1,
        )

        result = roi.astype(np.float32) * (1 - mask) + blurred.astype(np.float32) * mask
        result = result.astype(np.uint8)

        image[y1:y2, x1:x2] = result

    return image
