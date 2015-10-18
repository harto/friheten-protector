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
    width = int(config.get('FRAME_WIDTH'))
    ratio = width / float(orig_w)
    height = int(orig_h * ratio)
    return cv2.resize(image,
                      (width, height),
                      interpolation=cv2.INTER_AREA)

def process(image):
    # Discard colour information; irrelevant to motion detection
    processed = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Remove noise
    blur_kernel = (int(config.get('BLUR_KERNEL_WIDTH')),
                   int(config.get('BLUR_KERNEL_HEIGHT')))
    processed = cv2.GaussianBlur(processed, blur_kernel, 0)
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
                                int(config.get('MIN_CHANGE_THRESHOLD')),
                                255,
                                cv2.THRESH_BINARY)
        # dilate to join broken contours
        diff = cv2.dilate(diff, None, iterations=2)
        (_, contours, _) = cv2.findContours(diff,
                                            cv2.RETR_EXTERNAL,
                                            cv2.CHAIN_APPROX_SIMPLE)
        return [cv2.boundingRect(c) for c in contours
                if cv2.contourArea(c) >= int(config.get('MIN_CHANGE_AREA'))]

    def overlay_rect(self, rect):
        (x, y, w, h) = rect
        cv2.rectangle(self.raw,
                      (x, y),
                      (x + w, y + h),
                      color=(0, 0, 255),
                      thickness=2)

    def overlay_timestamp(self):
        cv2.putText(self.raw,
                    self.datetime.strftime('%Y-%m-%d %H:%M:%S'),
                    (10, self.raw.shape[0] - 10),
                    cv2.FONT_HERSHEY_PLAIN,
                    1,
                    (0, 0, 255))
