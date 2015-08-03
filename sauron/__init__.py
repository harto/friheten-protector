import numpy
import cv2
import os
import datetime
import time
import sauron.config
from sauron.config import get as get_config

def resize(image, width):
    orig_h, orig_w = image.shape[:2]
    ratio = width / float(orig_w)
    height = int(orig_h * ratio)
    return cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)

def preprocess_frame(frame):
    # Colour is irrelevant to motion detection
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Remove noise etc.
    frame = cv2.GaussianBlur(frame, get_config('BLUR_KERNEL'), 0)
    return frame

def obscured_regions(image):
    (_, contours, _) = cv2.findContours(image.copy(),
                                       cv2.RETR_EXTERNAL,
                                       cv2.CHAIN_APPROX_SIMPLE)
    return (cv2.boundingRect(c) for c in contours
            if cv2.contourArea(c) >= get_config('MIN_CHANGE_AREA'))

BACKGROUND = None

def process_frame(raw):
    global BACKGROUND
    frame = preprocess_frame(raw)
    if BACKGROUND is None:
        BACKGROUND = frame
    frame = cv2.absdiff(BACKGROUND, frame)
    _, frame = cv2.threshold(frame,
                             get_config('MIN_CHANGE_THRESHOLD'),
                             255,
                             cv2.THRESH_BINARY)
    # dilate to join broken contours
    frame = cv2.dilate(frame, None, iterations=2)
    rects = obscured_regions(frame)
    for (x, y, w, h) in rects:
        cv2.rectangle(raw, (x, y), (x + w, y + h), color=(0, 255, 0), thickness=2)
    cv2.imshow('raw', raw)
    cv2.imshow('filtered', frame)

def key_pressed(key):
    return cv2.waitKey(1) & 0xFF == ord(key)

def frames(input):
    while True:
        success, frame = input.read()
        if success:
            yield frame
        else:
            return

def finished():
    return key_pressed('q')

def process_video(input, output):
    for frame in frames(input):
        if finished(): break
        resized = resize(frame, width=get_config('INPUT_FRAME_WIDTH'))
        process_frame(resized)
        # output.write(resized)

if __name__ == '__main__':
    sauron.config.init()
    cam = cv2.VideoCapture(0)
    path = os.path.join(os.path.dirname(__file__), 'tmp', datetime.datetime.now().strftime('%Y-%m-%d-%H%M%S.mpg'))
    print 'writing to %s' % path
    output_codec = cv2.VideoWriter_fourcc(*get_config('OUTPUT_FORMAT')) #cv2.VideoWriter_fourcc(*'MPEG')
    file = cv2.VideoWriter(path,
                           output_codec,
                           get_config('OUTPUT_FPS'),
                           get_config('OUTPUT_FRAME_SIZE'),
                           True)
    time.sleep(2) # fixme: proper wait
    process_video(cam, file)
    cam.release()
    file.release()
    # cv2.destroyAllWindows()
