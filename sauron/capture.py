import cv2
from datetime import datetime
from sauron import config
import time

def read_frames(video):
    while True:
        success, image = video.read()
        if success:
            yield create_frame(image)
        else:
            break

def create_frame(image):
    raw = downscale(image)
    processed = process(raw)
    return Frame(raw, processed, time.time())

def downscale(image):
    orig_h, orig_w = image.shape[:2]
    width = config.get('FRAME_WIDTH')
    ratio = width / float(orig_w)
    height = int(orig_h * ratio)
    return cv2.resize(image,
                      (width, height),
                      interpolation=cv2.INTER_AREA)

def process(image):
    # Discard colour information; irrelevant to motion detection
    processed = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Remove noise
    processed = cv2.GaussianBlur(processed, config.get('BLUR_KERNEL'), 0)
    return processed

class Frame(object):

    def __init__(self, raw, processed, time):
        self.raw = raw
        self.processed = processed
        self.time = time

    @property
    def datetime(self):
        return datetime.fromtimestamp(self.time)

    def diffs(self, other):
        diff = cv2.absdiff(self.processed, other.processed)
        _, diff = cv2.threshold(diff,
                                config.get('MIN_CHANGE_THRESHOLD'),
                                255,
                                cv2.THRESH_BINARY)
        # dilate to join broken contours
        diff = cv2.dilate(diff, None, iterations=2)
        (_, contours, _) = cv2.findContours(diff,
                                            cv2.RETR_EXTERNAL,
                                            cv2.CHAIN_APPROX_SIMPLE)
        return [cv2.boundingRect(c) for c in contours
                if cv2.contourArea(c) >= config.get('MIN_CHANGE_AREA')]
