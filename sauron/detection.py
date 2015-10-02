import cv2
from datetime import datetime
from os import makedirs, path
from sauron.capture import read_frames
from sauron import config
from sauron.recording import Recording
import time

class Detector(object):

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
                self.recording.finish()
                self.state = 'waiting'

    def new_recording(self):
        output_dir = path.join(config.get('OUTPUT_DIR'),
                               datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))
        print 'writing to %s' % output_dir
        if not path.exists(output_dir): makedirs(output_dir)
        self.recording = Recording(output_dir)
        self.recording.write_image(self.background.raw)
