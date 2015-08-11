import cv2
from datetime import datetime
from os import makedirs, path
from sauron.capture import read_frames
from sauron import config
from sauron.recording import Recording
import time

background = None
state = 'waiting'
recording = None

def detect_motion(input):
    global background
    time.sleep(2) # fixme: await input initialisation
    frames = read_frames(input)
    frames.next() # eat first frame; sometimes corrupted
    background = frames.next()
    for frame in frames:
        process_frame(frame)

def process_frame(frame):
    global state, recording
    rects = find_diff_regions(background.processed, frame.processed)
    motion_detected = len(rects)

    if motion_detected:
        if state == 'waiting':
            state = 'capturing'
            recording = create_recording()
        recording.write(frame, rects)
    else:
        if state == 'capturing':
            state = 'waiting'
            recording.finish()

def find_diff_regions(a, b):
    diff = cv2.absdiff(a, b)
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

def create_recording():
    output_dir = path.join(config.get('OUTPUT_DIR'),
                           datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))
    print 'writing to %s' % output_dir
    makedirs(output_dir)
    return Recording(output_dir, background)
