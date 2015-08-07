import cv2
import time
from sauron import config
from sauron.video_input import read_frames

background = None
state = 'waiting'

def detect_motion(input):
    global background
    time.sleep(2) # fixme: await input initialisation
    frames = read_frames(input)
    background = frames.next()
    cv2.imshow('bg', background.raw)
    for frame in frames:
        analyse_frame(frame)

def process_frame(frame):
    global state
    rects = find_diff_regions(background.processed, frame.processed)
    motion_detected = len(rects)

    if motion_detected:
        if state == 'waiting':
            state = 'capturing'
            capture = init_capture()
        capture.write(frame, rects)
    else:
        if state == 'capturing':
            state = 'waiting'
            capture.close()
            capture.notify()

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
    return (cv2.boundingRect(c) for c in contours
            if cv2.contourArea(c) >= config.get('MIN_CHANGE_AREA'))
