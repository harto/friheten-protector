import numpy
import cv2
#import sys
import time

# fixme: better names
BLUR_KERNEL = (21, 21)
FRAME_WIDTH = 500
MIN_CHANGE_AREA = 500
MIN_CHANGE_THRESHOLD = 25

def resize(image, width):
    orig_h, orig_w = image.shape[:2]
    ratio = width / float(orig_w)
    height = int(orig_h * ratio)
    return cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)

def preprocess_frame(frame):
    frame = resize(frame, width=FRAME_WIDTH)
    # Colour is irrelevant to motion detection
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Remove noise etc.
    frame = cv2.GaussianBlur(frame, BLUR_KERNEL, 0)
    return frame

def obscured_regions(image):
    (_, contours, _) = cv2.findContours(image.copy(),
                                        cv2.RETR_EXTERNAL,
                                        cv2.CHAIN_APPROX_SIMPLE)
    return (cv2.boundingRect(c) for c in contours
            if cv2.contourArea(c) >= MIN_CHANGE_AREA)

BACKGROUND = None

def process_frame(raw):
    global BACKGROUND
    frame = preprocess_frame(raw)
    if BACKGROUND is None:
        BACKGROUND = frame
    frame = cv2.absdiff(BACKGROUND, frame)
    _, frame = cv2.threshold(frame, CHANGE_THRESHOLD, 255, cv2.THRESH_BINARY)
    # dilate to join broken contours
    frame = cv2.dilate(frame, None, iterations=2)
    rects = obscured_regions(frame)
    for (x, y, w, h) in rects:
        cv2.rectangle(raw, (x, y), (x + w, y + h), color=(0, 255, 0), thickness=2)
    cv2.imshow('raw', raw)
    cv2.imshow('filtered', frame)

def finished():
    return cv2.waitKey(1) & 0xFF == ord('q')

def process_video(video):
    while True:
        success, frame = video.read()
        if not success or finished():
            break
        process_frame(frame)

if __name__ == '__main__':
    cam = cv2.VideoCapture(0)
    time.sleep(0.25) # fixme
    process_video(cam)
    cv2.destroyAllWindows()
    cam.release()
