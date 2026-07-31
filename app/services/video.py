import cv2
import tempfile
from pathlib import Path


class Video:
    def __init__(self, upload, suffix):
        self._input = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
        upload.save(self._input.name)

        self.capture = cv2.VideoCapture(self._input.name)
        if not self.capture.isOpened():
            raise RuntimeError("Invalid Video")

        self.width = int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps = self.capture.get(cv2.CAP_PROP_FPS)
        self.frame_count = int(self.capture.get(cv2.CAP_PROP_FRAME_COUNT))

        self.output_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4").name
        self.writer = cv2.VideoWriter(
            self.output_path,
            cv2.VideoWriter_fourcc(*"avc1"),
            self.fps,
            (self.width, self.height),
        )

        if not self.writer.isOpened():
            raise RuntimeError("Could not create video writer")

    def frames(self):
        while True:
            success, frame = self.capture.read()
            if not success:
                break

            yield frame

    def read(self):
        with open(self.output_path, "rb") as f:
            return f.read()

    def write(self, frame):
        self.writer.write(frame)

    def close(self):
        self.capture.release()
        self.writer.release()
