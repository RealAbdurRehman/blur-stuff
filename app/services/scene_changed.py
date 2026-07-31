import cv2


def scene_changed(previous, current, threshold=20):
    if previous is None:
        return True

    previous = cv2.cvtColor(previous, cv2.COLOR_BGR2GRAY)
    previous = cv2.resize(previous, (320, 180))

    current = cv2.cvtColor(current, cv2.COLOR_BGR2GRAY)
    current = cv2.resize(current, (320, 180))

    difference = cv2.absdiff(previous, current)
    score = difference.mean()

    return score > threshold
