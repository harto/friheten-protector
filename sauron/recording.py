import cv2
from datetime import datetime
from os import path
from sauron import config
import time

class Recording(object):

    @classmethod
    def create(cls):
        recording_path = path.join(config.get('OUTPUT_DIR'),
                                   datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))
        print 'writing to %s' % recording_path
        return cls(recording_path)

    def __init__(self, path):
        self.path = path
        self.fps = FpsCounter()

    def write(self, frame, rects):
        raw = frame.raw
        for (x, y, w, h) in rects:
            cv2.rectangle(raw,
                          (x, y),
                          (x + w, y + h),
                          color=(0, 0, 255),
                          thickness=2)
        self.fps.increment()


    def finish(self):
        print 'finalising recording'


class FpsCounter(object):

    def __init__(self):
        self.count = 0
        self.last_tick = time.time()

    def increment(self):
        now = time.time()
        if now - self.last_tick > 1.0:
            print 'fps = %d' % self.count
            self.count = 0
            self.last_tick = now
        self.count += 1
