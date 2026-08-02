from .tracker.manager import TrackerManager
from .scene_changed import scene_changed


class VideoState:
    def __init__(self, detection_interval=1):
        self.detection_interval = detection_interval
        self.frame_number = 0
        self.previous_frame = None
        self.tracker = TrackerManager()

    def next_frame(self, frame):
        self.previous_frame = frame.copy()
        self.frame_number += 1

    def should_detect(self, frame, tracker_lost):
        return (
            self.frame_number == 0
            or self.frame_number % self.detection_interval == 0
            or tracker_lost
            or scene_changed(self.previous_frame, frame)
        )
