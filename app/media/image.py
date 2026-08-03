class Image:
    def __init__(self, image=None, frames=None, durations=None, loop=0):
        self.image = image
        self.frames = frames
        self.durations = durations
        self.loop = loop

    @property
    def animated(self):
        return self.frames is not None
