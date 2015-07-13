import numpy
import cv2
#import sys

BACKGROUND = None

def finished():
    return cv2.waitKey(1) & 0xFF == ord('q')

def resize(image, width):
    orig_h, orig_w = image.shape[:2]
    ratio = width / float(orig_w)
    height = int(orig_h * ratio)
    return cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)

def preprocess_frame(frame):
    frame = resize(frame, width=500)
    # Colour is irrelevant to motion detection
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Remove noise etc.
    frame = cv2.GaussianBlur(frame, (21, 21), 0)
    return frame

def process_frame(frame):
    global BACKGROUND
    frame = preprocess_frame(frame)
    if BACKGROUND is None:
        BACKGROUND = frame
    # delta = cv2.absdiff(BACKGROUND, frame)
    cv2.imshow('frame', frame)

def process_video(video):
    while True:
        success, frame = video.read()
        if not success or finished():
            break
        process_frame(frame)

if __name__ == '__main__':
    cam = cv2.VideoCapture(0)
    process_video(cam)
    cam.release()
