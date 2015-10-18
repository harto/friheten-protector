import numpy
import cv2
from sauron import config
from sauron.capture import read_frames
from sauron.detection import MotionDetector
import signal
import time

if __name__ == '__main__':
    config.init()

    camera = cv2.VideoCapture(0)
    time.sleep(2)
    frames = read_frames(camera)
    # eat first frame; sometimes corrupted
    _ = frames.next()

    detector = MotionDetector(frames)

    def finish():
        detector.finish()
        camera.release()
        exit(0)

    handler = lambda sig, stack_frame: finish()
    signal.signal(signal.SIGHUP, handler)
    signal.signal(signal.SIGTERM, handler)

    try:
        detector.detect()
    except KeyboardInterrupt:
        pass

    finish()
