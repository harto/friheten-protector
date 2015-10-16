import numpy
import cv2
from sauron import config
from sauron.capture import read_frames
from sauron.detection import MotionDetector
import time

if __name__ == '__main__':
    config.init()
    camera = cv2.VideoCapture(0)
    time.sleep(0.5)
    frames = read_frames(camera)
    # eat first frame; sometimes corrupted
    _ = frames.next()
    try:
        MotionDetector(frames).detect()
    except KeyboardInterrupt:
        # todo: clean up gracefully
        pass
    camera.release()
