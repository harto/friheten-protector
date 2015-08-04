import cv2
import time
from sauron.config import get as get_config

BACKGROUND = None

def detect_motion(input):
    global BACKGROUND
    time.sleep(2) # fixme: await input initialisation
    frames = read_frames(input)
    BACKGROUND = frames.next()
    cv2.imshow('bg', BACKGROUND.raw)
    for frame in frames:
        process_frame(frame)

def process_frame(frame):
    rects = differing_rects(BACKGROUND.processed, frame.processed)
    raw = frame.raw
    for (x, y, w, h) in rects:
        cv2.rectangle(raw,
                      (x, y),
                      (x + w, y + h),
                      color=(0, 0, 255),
                      thickness=2)
        cv2.imshow('raw', raw)

def read_frames(input):
    while True:
        success, image = input.read()
        if success:
            yield create_frame(image)
        else:
            break

class Frame(object):
    def __init__(self, raw, processed):
        self.raw = raw
        self.processed = processed

def create_frame(image):
    raw = downscale(image)
    processed = process(raw)
    return Frame(raw, processed)

def downscale(image):
    orig_h, orig_w = image.shape[:2]
    width = get_config('FRAME_WIDTH')
    ratio = width / float(orig_w)
    height = int(orig_h * ratio)
    return cv2.resize(image,
                      (width, height),
                      interpolation=cv2.INTER_AREA)

def process(image):
    # Discard colour information; irrelevant to motion detection
    processed = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Remove noise
    processed = cv2.GaussianBlur(processed, get_config('BLUR_KERNEL'), 0)
    return processed

def differing_rects(a, b):
    diff = cv2.absdiff(a, b)
    _, diff = cv2.threshold(diff,
                            get_config('MIN_CHANGE_THRESHOLD'),
                            255,
                            cv2.THRESH_BINARY)
    # dilate to join broken contours
    diff = cv2.dilate(diff, None, iterations=2)
    (_, contours, _) = cv2.findContours(diff,
                                        cv2.RETR_EXTERNAL,
                                        cv2.CHAIN_APPROX_SIMPLE)
    return (cv2.boundingRect(c) for c in contours
            if cv2.contourArea(c) >= get_config('MIN_CHANGE_AREA'))
