import numpy
import cv2
from sauron import config
from sauron.detection import MotionDetector

if __name__ == '__main__':
    config.init()
    camera = cv2.VideoCapture(0)
    try:
        MotionDetector(camera).detect()
    except KeyboardInterrupt:
        pass
    camera.release()
