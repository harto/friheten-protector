import cv2
from sauron.capture import read_frames
from sauron.recording import Recording
import time

class MotionDetector(object):

    def __init__(self, source):
        self.source = source
        self.background = None
        self.recording = None
        self.state = 'waiting'

    def detect(self):
        self.setup()
        for frame in self.frames():
            self.process_frame(frame)

    def setup(self):
        time.sleep(1) # fixme: await input initialisation
        frames = self.frames()
        _ = frames.next() # eat first frame; sometimes corrupted
        self.background = frames.next()

    def frames(self):
        return read_frames(self.source)

    def process_frame(self, frame):
        diffs = self.background.diffs(frame)
        if len(diffs):
            if self.state == 'waiting':
                self.state = 'capturing'
                self.new_recording()
            self.recording.write(frame, diffs)
        else:
            if self.state == 'capturing':
                self.recording.finalise()
                self.state = 'waiting'

    def new_recording(self):
        self.recording = Recording.setup()
        self.recording.write_image(self.background.raw)
