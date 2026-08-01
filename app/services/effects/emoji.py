import cv2
from pathlib import Path

from .apply import overlay_image

ASSETS = Path(__file__).parent / "assets"
EMOJI = cv2.imread(str(ASSETS / "smile.png"), cv2.IMREAD_UNCHANGED)


def emoji_regions(image, boxes, padding=0):
    return overlay_image(image, boxes, EMOJI, padding)
