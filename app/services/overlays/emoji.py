import cv2
from pathlib import Path

from .apply import apply_overlay

ASSETS = Path(__file__).parent / "assets"
EMOJI = cv2.imread(str(ASSETS / "smile.png"), cv2.IMREAD_UNCHANGED)


def emoji_regions(image, boxes, padding=0):
    return apply_overlay(image, boxes, EMOJI, padding)
