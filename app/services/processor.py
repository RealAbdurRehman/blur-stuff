import cv2
import numpy as np


def grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
