import cv2
from sauron import config

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
    return Frame(raw, processed)

class Frame(object):
    def __init__(self, raw, processed):
        self.raw = raw
        self.processed = processed

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
